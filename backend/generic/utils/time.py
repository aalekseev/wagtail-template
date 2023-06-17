import calendar
import datetime
from datetime import timedelta

from dateutil.relativedelta import relativedelta


def get_full_month_range(date):
    first_day = date.replace(day=1)
    last_day = date.replace(day=calendar.monthrange(date.year, date.month)[1])
    return first_day, last_day


def get_current_week_number() -> str:
    return datetime.date.today().strftime("%V")


def seconds_to_hours(seconds: float) -> str:
    if seconds is None or seconds < 1:
        return ""
    return f"{(timedelta(seconds=seconds) / timedelta(hours=1)):.2f}"


def seconds_to_days(seconds: int) -> str:
    if seconds is None or seconds == 0:
        return ""
    return f"{(timedelta(seconds=seconds) / timedelta(hours=24)):.2f}"


def get_monthly_range(months=1):
    now = datetime.date.today()
    before = now - relativedelta(months=months)
    return now, before
