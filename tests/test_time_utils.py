# tests/test_time_utils.py

import unittest
from datetime import datetime, timedelta
from app.utils.time_utils import get_current_time, get_default_time_zone
import pytz



class TestTimeUtils(unittest.TestCase):

    def test_get_default_time_zone(self):
        # Test that the default time zone is 'Asia/Singapore'
        self.assertEqual(get_default_time_zone(), 'Asia/Singapore')

    def test_get_current_time(self):
        # Test that the current time is returned with the Singapore time zone
        singapore_tz = pytz.timezone('Asia/Singapore')
        current_time = get_current_time()

        self.assertEqual(current_time.tzinfo.zone, singapore_tz.zone)
        self.assertTrue(current_time >= datetime.now(
            singapore_tz) - timedelta(minutes=1))
        self.assertTrue(current_time <= datetime.now(
            singapore_tz) + timedelta(minutes=1))

    
    def test_get_current_time_with_correct_format(self):
        # Test that the current time is in the correct format
        current_time = get_current_time()
        self.assertIsInstance(current_time, datetime)
        self.assertEqual(current_time.tzinfo.zone, 'Asia/Singapore')


if __name__ == '__main__':
    unittest.main()
