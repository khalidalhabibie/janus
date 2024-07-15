from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify
from . import db
from .models import Event
from datetime import datetime
import uuid
from .utils.email_utils import validate_and_get_recipients
from .utils.time_utils import get_default_time_zone
import pytz
from pytz import timezone, UTC
from sqlalchemy import desc
from flask import Flask, send_from_directory

main = Blueprint('main', __name__)


@main.route('/')
def index():
    events = Event.query.order_by(desc(Event.expected_sent_at)).all()
    tz = timezone(get_default_time_zone())

    for event in events:
        if event.expected_sent_at.tzinfo is None:
            event.expected_sent_at = event.expected_sent_at.replace(tzinfo=UTC)
        event.expected_sent_at = event.expected_sent_at.astimezone(
            tz)

    return render_template('index.html', events=events)


@main.route('/add', methods=['GET', 'POST'])
def add_email():
    if request.method == 'POST':
        email_subject = request.form.get('email_subject')
        email_content = request.form.get('email_content')
        expected_sent_at = request.form.get('send_at')
        recipients_str = request.form.get('recipients')
        _, error = validate_and_get_recipients(recipients_str)
        if error:
            flash(error, 'error')
            return redirect(url_for('main.add_email'))

        event_id = str(uuid.uuid4())

        tz = pytz.timezone(get_default_time_zone())

        try:
            send_at = datetime.fromisoformat(expected_sent_at)
            send_at = tz.localize(send_at)
        except ValueError:
            return jsonify({'error': 'Invalid datetime format. Use ISO 8601 format.'}), 400

        new_event = Event(
            event_id=event_id,
            email_subject=email_subject,
            email_content=email_content,
            expected_sent_at=send_at,
            recipients=recipients_str
        )

        db.session.add(new_event)
        db.session.commit()
        flash('Email scheduled successfully!', 'success')
        return redirect(url_for('main.index'))

    return render_template('add_email.html')


@main.route('/api/events', methods=['POST'])
def save_emails():
    data = request.get_json()

    # Validate and get recipients
    recipients_str = data.get('recipients', '')
    _, error = validate_and_get_recipients(recipients_str)
    if error:
        return jsonify({'error': error}), 400

    email_subject = data.get('email_subject')
    email_content = data.get('email_content')
    expected_sent_at_str = data.get('expected_sent_at')

    if not email_subject or not email_content or not expected_sent_at_str:
        return jsonify({'error': 'Missing required fields.'}), 400

    tz = pytz.timezone(get_default_time_zone())

    try:
        expected_sent_at_naive = datetime.fromisoformat(expected_sent_at_str)
        expected_sent_at = tz.localize(expected_sent_at_naive)
    except ValueError:
        return jsonify({'error': 'Invalid datetime format. Use ISO 8601 format.'}), 400

    event_id = str(uuid.uuid4())

    new_event = Event(
        event_id=event_id,
        email_subject=email_subject,
        email_content=email_content,
        expected_sent_at=expected_sent_at,
        recipients=recipients_str
    )

    db.session.add(new_event)
    db.session.commit()
    return jsonify({"status": "success", "message": "Email scheduled successfully"}), 201


@main.route('/swagger/swagger.yaml')
def swagger_yaml():
    return send_from_directory('swagger', 'swagger.yaml')
