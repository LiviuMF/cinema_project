from django.contrib import admin
from .models import Movie, ContactMessages, Hall, Schedule, Reservation, Cinema, Seat

admin.site.register(Cinema)
admin.site.register(ContactMessages)
admin.site.register(Hall)
admin.site.register(Movie)
admin.site.register(Reservation)
admin.site.register(Schedule)
admin.site.register(Seat)

