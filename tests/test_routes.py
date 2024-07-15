# tests/test_routes.py

import unittest
from app import create_app, db
from app.models import Event
from app.utils.email_utils import validate_and_get_recipients
from app.utils.time_utils import get_default_time_zone
from datetime import datetime
import pytz
import uuid


class TestRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()  # Adjusted to call create_app() without arguments
        cls.client = cls.app.test_client()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()

    def setUp(self):
        db.create_all()
        # Add initial data if necessary
        self.tz = pytz.timezone(get_default_time_zone())

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_index(self):
        # Create a sample event
        expected_sent_at = datetime(2024, 8, 1, 10, 0, 0, tzinfo=self.tz)
        event = Event(
            event_id="12345678-1234-1234-1234-1234567890ab",
            email_subject="Test Subject",
            email_content="Test Content",
            expected_sent_at=expected_sent_at,
            recipients="test@example.com"
        )
        db.session.add(event)
        db.session.commit()

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Subject', response.data)
        self.assertIn(b'Test Content', response.data)

    def test_add_email_post_fail_invalid_datetime(self):
        data = {
            'email_subject': 'Test Subject',
            'email_content': 'Test Content',
            'send_at': 'Invalid datetime format',
            'recipients': 'test@example.com'
        }

        response = self.client.post('/add', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            b'Invalid datetime format. Use ISO 8601 format.', response.data)

    def test_save_emails_post_success(self):
        data = {
            'email_subject': 'Test Subject',
            'email_content': 'Test Content',
            'expected_sent_at': '2024-08-01T10:00:00',
            'recipients': 'test@example.com'
        }

        response = self.client.post('/api/events', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {
                         'status': 'success', 'message': 'Email scheduled successfully'})

        event = Event.query.first()
        self.assertIsNotNone(event)
        self.assertEqual(event.email_subject, 'Test Subject')
        self.assertEqual(event.email_content, 'Test Content')
        self.assertEqual(event.recipients, 'test@example.com')

    def test_save_emails_post_fail_missing_fields(self):
        data = {
            'email_subject': 'Test Subject',
            'email_content': 'Test Content',
            # Missing 'expected_sent_at' field
            'recipients': 'test@example.com'
        }

        response = self.client.post('/api/events', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing required fields.', response.data)

    def test_save_emails_post_fail_invalid_datetime(self):
        data = {
            'email_subject': 'Test Subject',
            'email_content': 'Test Content',
            'expected_sent_at': 'Invalid datetime format',
            'recipients': 'test@example.com'
        }

        response = self.client.post('/api/events', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            b'Invalid datetime format. Use ISO 8601 format.', response.data)

    


if __name__ == '__main__':
    unittest.main()
