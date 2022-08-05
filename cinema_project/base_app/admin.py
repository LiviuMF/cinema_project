from import_export.admin import ImportExportModelAdmin

from django.contrib import admin
from .models import Movie, ContactMessages, Hall, Schedule, Reservation, Cinema, Seat

admin.site.register(Cinema)
admin.site.register(ContactMessages)
admin.site.register(Hall)
admin.site.register(Reservation)
admin.site.register(Schedule)
admin.site.register(Seat)


@admin.register(Movie)
class MovieAdmin(ImportExportModelAdmin):
    list_display = ('name', 'poster_url', 'poster_image', 'description', 'year',
                    'director', 'imdb_link', 'imdb_id', 'imdb_rating', 'duration', 'trailer_id')
    pass

