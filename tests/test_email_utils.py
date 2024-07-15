# tests/test_email_utils.py

import unittest
from app.utils.email_utils import is_valid_email, validate_and_get_recipients


class TestEmailUtils(unittest.TestCase):

    def test_is_valid_email(self):
        # Valid emails
        self.assertTrue(is_valid_email('test@example.com'))
        self.assertTrue(is_valid_email('test.email+alex@leetcode.com'))

        # Invalid emails
        self.assertFalse(is_valid_email('plainaddress'))
        self.assertFalse(is_valid_email('@missingusername.com'))
        self.assertFalse(is_valid_email('username@.com'))

    def test_validate_and_get_recipients(self):
        # Valid input
        recipients, error = validate_and_get_recipients(
            'test@example.com, valid@example.com')
        self.assertEqual(recipients, ['test@example.com', 'valid@example.com'])
        self.assertIsNone(error)

        # Invalid input
        recipients, error = validate_and_get_recipients(
            'test@example.com, invalidemail.com')
        self.assertIsNone(recipients)
        self.assertEqual(error, 'Invalid emails: invalidemail.com')

        # Empty input
        recipients, error = validate_and_get_recipients('')
        self.assertEqual(recipients, [])
        self.assertEqual(error, 'Recipients are required.')


if __name__ == '__main__':
    unittest.main()
