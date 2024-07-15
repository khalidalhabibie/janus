# app/utils/time_utils.py
from datetime import datetime
import pytz


def get_current_time():
    singapore_tz = pytz.timezone(get_default_time_zone())
    return datetime.now(singapore_tz)

def get_default_time_zone():
    return 'Asia/Singapore'
