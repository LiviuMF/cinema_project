import datetime


def today() -> datetime:
    return datetime.datetime.today()


def days_ago(days: int) -> datetime:
    now = today()
    return now - datetime.timedelta(days=days)
