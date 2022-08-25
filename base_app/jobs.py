from .models import Reservation
from cinema_project.utils import thirty_minutes_ahead

from apscheduler.schedulers.background import BackgroundScheduler


def cancel_unconfirmed_reservations() -> None:
    Reservation.objects.filter(
        is_confirmed=False,
        is_canceled=False,
        schedule__schedule_time__lte=thirty_minutes_ahead()
    ).update(is_canceled=True)


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(cancel_unconfirmed_reservations, 'interval', minutes=1)
    scheduler.start()
