from .models import Reservation
from .utils import thirty_minutes_ahead

from apscheduler.schedulers.background import BackgroundScheduler


def cancel_unconfirmed_reservations() -> None:
    reservations_to_cancel = Reservation.objects.filter(
        is_confirmed=False,
        is_canceled=False,
        schedule__schedule_time__lte=thirty_minutes_ahead()
    )
    for reservation in reservations_to_cancel:
        reservation.is_canceled = True
        reservation.save()


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(cancel_unconfirmed_reservations, 'interval', minutes=1)
    scheduler.start()
