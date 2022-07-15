import datetime


def today() -> datetime:
    return datetime.datetime.today()


def next_days(days: int) -> datetime:
    now = today()
    return now + datetime.timedelta(days= days)

