# tests/test_tasks.py

import unittest
from unittest.mock import patch, MagicMock
from app import create_app
from app.tasks import send_email, send_scheduled_emails
from app.models import Event
from app.utils.time_utils import get_current_time
from datetime import datetime, timezone


class TestTasks(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the application for the test cases."""
        cls.app = create_app()  # Ensure create_app initializes the Flask app
        cls.app.app_context().push()  # Push the app context for the test cases

    @patch('app.tasks.mail.send')
    @patch('app.tasks.get_current_time')
    def test_send_email_success(self, mock_get_current_time, mock_mail_send):
        """Test send_email function for successful email sending."""
        # Setup mock
        mock_get_current_time.return_value = datetime(
            2024, 8, 1, 10, 0, 0, tzinfo=timezone.utc)

        # Create a mock event
        event = Event(
            event_id="12345678-1234-1234-1234-1234567890ab",
            email_subject="Test Subject",
            email_content="Test Content",
            expected_sent_at=datetime(
                2024, 8, 1, 10, 0, 0, tzinfo=timezone.utc),
            recipients="test@example.com"
        )

        # Call send_email function
        send_email(event, self.app)

        # Assertions
        mock_mail_send.assert_called_once()
        self.assertTrue(event.is_sent)
        self.assertEqual(event.exactly_sent_at, datetime(
            2024, 8, 1, 10, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(event.updated_at, datetime(
            2024, 8, 1, 10, 0, 0, tzinfo=timezone.utc))
        self.assertFalse(event.is_failed)
        self.assertIsNone(event.error_message)

    @patch('app.tasks.mail.send')
    @patch('app.tasks.get_current_time')
    def test_send_email_failure(self, mock_get_current_time, mock_mail_send):
        """Test send_email function for failure scenario."""
        # Setup mock
        mock_get_current_time.return_value = datetime(
            2024, 8, 1, 10, 0, 0, tzinfo=timezone.utc)
        mock_mail_send.side_effect = Exception("Email sending failed")

        # Create a mock event
        event = Event(
            event_id="12345678-1234-1234-1234-1234567890ab",
            email_subject="Test Subject",
            email_content="Test Content",
            expected_sent_at=datetime(
                2024, 8, 1, 10, 0, 0, tzinfo=timezone.utc),
            recipients="test@example.com"
        )

        # Call send_email function
        send_email(event, self.app)

        # Assertions
        mock_mail_send.assert_called_once()
        self.assertTrue(event.is_failed)
        self.assertEqual(event.error_message, "Email sending failed")
        self.assertEqual(event.updated_at, datetime(
            2024, 8, 1, 10, 0, 0, tzinfo=timezone.utc))

    @patch('app.tasks.send_email')
    @patch('app.tasks.get_current_time')
    def test_send_scheduled_emails(self, mock_get_current_time, mock_send_email):
        """Test send_scheduled_emails function."""
        # Setup mocks
        mock_get_current_time.return_value = datetime(
            2024, 8, 1, 10, 0, 0, tzinfo=timezone.utc)

        # Create some mock events
        event1 = Event(
            event_id="12345678-1234-1234-1234-1234567890ab",
            email_subject="Test Subject 1",
            email_content="Test Content 1",
            expected_sent_at=datetime(
                2024, 8, 1, 9, 0, 0, tzinfo=timezone.utc),
            recipients="test1@example.com"
        )
        event2 = Event(
            event_id="23456789-2345-2345-2345-234567890abc",
            email_subject="Test Subject 2",
            email_content="Test Content 2",
            expected_sent_at=datetime(
                2024, 8, 1, 10, 0, 0, tzinfo=timezone.utc),
            recipients="test2@example.com"
        )

        # Mock Event.query
        with patch('app.tasks.Event.query') as mock_query:
            mock_query.filter.return_value.all.return_value = [event1, event2]

            # Call send_scheduled_emails function
            send_scheduled_emails(self.app)

            # Assertions
            mock_send_email.assert_any_call(event1, self.app)
            mock_send_email.assert_any_call(event2, self.app)
            self.assertEqual(mock_send_email.call_count, 2)

    @patch('app.tasks.send_scheduled_emails')
    @patch('app.tasks.get_current_time')
    def test_send_scheduled_emails_no_events(self, mock_get_current_time, mock_send_scheduled_emails):
        """Test send_scheduled_emails function when there are no events."""
        # Setup mocks
        mock_get_current_time.return_value = datetime(
            2024, 8, 1, 10, 0, 0, tzinfo=timezone.utc)

        # Mock Event.query to return no events
        with patch('app.tasks.Event.query') as mock_query:
            mock_query.filter.return_value.all.return_value = []

            # Call send_scheduled_emails function
            send_scheduled_emails(self.app)

            # Assertions
            mock_send_scheduled_emails.assert_not_called()


if __name__ == '__main__':
    unittest.main()
