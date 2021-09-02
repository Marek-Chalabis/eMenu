import random
import time
from datetime import datetime, timedelta
from typing import Optional


def get_random_date(
        start_date: Optional[datetime] = None
) -> datetime:
    """By default from last 14 days."""
    time_format = '%m/%d/%Y %I:%M %p'
    start_date = start_date or datetime.now() - timedelta(
        seconds=14 * 24 * 60 * 60
    )
    start_time = time.mktime(
        time.strptime(start_date.strftime(time_format), time_format)
    )
    end_time = time.mktime(
        time.strptime(datetime.now().strftime(time_format), time_format)
    )
    seconds = start_time + random.random() * (end_time - start_time)
    date_str = time.strftime(time_format, time.localtime(seconds))
    return datetime.strptime(date_str, time_format)
