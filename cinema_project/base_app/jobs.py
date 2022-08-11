from .models import Reservation
from .utils import thirty_minutes_ahead

from apscheduler.schedulers.background import BackgroundScheduler


def remove_unconfirmed_reservations() -> None:
    Reservation.objects.filter(
        is_confirmed=False,
        schedule__schedule_time__lte=thirty_minutes_ahead()
    ).delete()


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(remove_unconfirmed_reservations, 'interval', minutes=1)
    scheduler.start()
