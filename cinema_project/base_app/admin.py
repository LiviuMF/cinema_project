from django.contrib import admin
from .models import Movie, ContactMessages, Hall, Schedule, Reservation

admin.site.register(Movie)
admin.site.register(ContactMessages)
admin.site.register(Hall)
admin.site.register(Schedule)
admin.site.register(Reservation)
