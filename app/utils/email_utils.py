# app/utils/email_utils.py

import re
from flask import request, jsonify


def is_valid_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None


def validate_and_get_recipients(recipients_str):
    if not recipients_str:
        return [], 'Recipients are required.'

    recipients = [email.strip() for email in recipients_str.split(',')]
    invalid_emails = [
        email for email in recipients if not is_valid_email(email)]
    if invalid_emails:
        return None, f"Invalid emails: {', '.join(invalid_emails)}"
    return recipients, None
