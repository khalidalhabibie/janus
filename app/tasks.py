from flask import current_app
from datetime import datetime, timezone
from flask_mail import Message
from .models import Event
from .db import db
from .mail import mail
from .utils.time_utils import get_current_time


def send_email(event, app):
    with app.app_context():
        recipients = event.recipients.split(',')
        message = Message(
            subject=event.email_subject,
            recipients=recipients,
            body=event.email_content
        )
        now = get_current_time()
        try:
            mail.send(message)
            print("Email sent to:", recipients)
            event.is_sent = True
            event.updated_at = now
            event.exactly_sent_at = now
            db.session.commit()
        except Exception as e:
            event.is_failed = True
            event.error_message = str(e)
            event.updated_at = now
            db.session.commit()
            print(str(e))


def send_scheduled_emails(app):
    with app.app_context():
        now = get_current_time()
        print("now :  ",
              now)
        events = Event.query.filter(Event.expected_sent_at <= now, Event.is_sent ==
                                    False, Event.is_failed == False, Event.deleted_at == None).all()

        print("event count : ", len(events))
        for event in events:
            send_email(event, app)
