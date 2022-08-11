import csv
import io

from django.contrib import admin
from django import forms
from django.shortcuts import render, redirect
from django.urls import path

from .models import Movie, ContactMessages, Hall, Schedule, Reservation, Cinema, Seat


class CsvImport(forms.Form):
    file_upload = forms.FileField()


class MovieAdmin(admin.ModelAdmin):
    list_display = ('name', 'poster_url', 'poster_image', 'description',
                    'year', 'director', 'imdb_link', 'imdb_id', 'imdb_rating',
                    'duration', 'trailer_id')
    change_list_template = "admin/base_app/movie/change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            uploaded_file = request.FILES['file_upload']
            csv_file = uploaded_file.read().decode('utf-8')
            reader = csv.DictReader(io.StringIO(csv_file))
            for row in reader:
                movie = Movie(
                            name=row['name'],
                            poster_url=row['poster_url'],
                            poster_image=row['poster_image'],
                            description=row['description'],
                            year=row['year'],
                            director=row['director'],
                            imdb_link=row['imdb_link'],
                            imdb_id=row['imdb_id'],
                            imdb_rating=row['imdb_rating'],
                            duration=row['duration'],
                            trailer_id=row['trailer_id'],
                )
                movie.save()
            self.message_user(request, "Your csv file has been imported")
            return redirect("..")
        form = CsvImport()
        payload = {"form": form}
        return render(
            request, "admin/csv_upload.html", payload
        )


admin.site.register(Reservation)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Cinema)
admin.site.register(ContactMessages)
admin.site.register(Hall)
admin.site.register(Schedule)
admin.site.register(Seat)
