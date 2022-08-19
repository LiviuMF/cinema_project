import os
from zipfile import ZipFile

from django.contrib import admin
from django.core.files.images import ImageFile
from django import forms
from django.shortcuts import render, redirect
from django.urls import path

from .models import Movie, ContactMessages, Hall, Schedule, Reservation, Cinema, Seat
from cinema_project.utils import fetch_from_csv, send_email


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
            path('import-zip/', self.import_zip)
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            uploaded_file = request.FILES['file_upload']
            movies_from_csv = fetch_from_csv(uploaded_file)
            existing_movie_ids = [movie_obj.imdb_id for movie_obj in Movie.objects.all()]

            movies_to_upload = [movie_obj for movie_obj in movies_from_csv
                                if movie_obj['imdb_id'] not in existing_movie_ids]

            Movie.objects.bulk_create([
                Movie(
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
                        ) for row in movies_to_upload])

            duplicate_movie_ids = [movie_obj['imdb_id'] for movie_obj in movies_from_csv
                                   if movie_obj['imdb_id'] in existing_movie_ids]
            is_duplicates = len(duplicate_movie_ids) > 0

            movie_upload_finished_message = '' if not is_duplicates else \
                "<p>==>Movie already in db: " \
                "Movies that have not been uploaded as they are duplicates in db</p>" \
                "<br/>" \
                + ",".join(duplicate_movie_ids)

            send_email(
                from_email='cinemaX@test.ro',
                to_email='liviu.m.farcas@gmail.com',
                subject='Your movie import statistics',
                html_content=f"Hello,"
                             "<p>Your movies have been uploaded successfully!</p>"
                             f"{movie_upload_finished_message}"
                             '<br/><p>Have a good one!</p>'
                             '<br/> Cinema X'
            )
            self.message_user(request, "Your csv file has been imported")
            return redirect("..")
        form = CsvImport()
        payload = {"form": form}
        return render(
            request, "admin/csv_upload.html", payload
        )

    def import_zip(self, request):
        if request.method == "POST":
            zip_file = request.FILES['file_upload']
            with ZipFile(zip_file, 'r') as _zip:
                # fetch csv from zip file
                zip_path_to_csv = [file for file in _zip.infolist() if '.csv' in file.filename]
                csv_file = _zip.open(zip_path_to_csv[0])
                movies_from_csv = fetch_from_csv(csv_file)
                existing_movie_ids = [movie_obj.imdb_id for movie_obj in Movie.objects.all()]

                movies_to_upload = [movie_obj for movie_obj in movies_from_csv
                                    if movie_obj['imdb_id'] not in existing_movie_ids]

                # fetch images from zip file
                image_types = ['.png', 'jpg', '.jpeg']
                images_in_zip = [file for file in _zip.infolist() if
                                 any(image_type in file.filename for image_type in image_types)]
                # make sure images are saved in root and not directory structure from zip
                for image in images_in_zip:
                    image.filename = os.path.basename(image.filename)

                def fetch_image_for_imdb_id(imdb_id: str):
                    try:
                        movie_image = [_zip.open(image) for image in images_in_zip if imdb_id in image.filename][0]
                        return ImageFile(movie_image)
                    except IndexError:
                        return '/images/default_poster.jpg'

                Movie.objects.bulk_create([
                    Movie(
                        name=row['name'],
                        poster_url=row['imdb_link'],
                        poster_image=fetch_image_for_imdb_id(row['imdb_id']),
                        description=row['description'],
                        year=row['year'],
                        director=row['director'],
                        imdb_link=row['imdb_link'],
                        imdb_id=row['imdb_id'],
                        imdb_rating=row['imdb_rating'],
                        duration=row['duration'],
                        trailer_id=row['trailer_id'],
                    ) for row in movies_to_upload])

            # notify user of import results
            movies_without_images = Movie.objects.filter(poster_image='/images/default_poster.jpg')
            duplicate_movie_ids = [movie_obj['imdb_id'] for movie_obj in movies_from_csv
                                   if movie_obj['imdb_id'] in existing_movie_ids]
            is_duplicates = len(duplicate_movie_ids) > 0
            is_without_image = len(movies_without_images) > 0

            duplicate_movie_message = '' if not is_duplicates else \
                                      "<p>==>Movie already in db: "\
                                      "Movies that have not been uploaded as they are duplicates in db</p>"\
                                      "<br/>"\
                                      + ",".join(duplicate_movie_ids)
            no_image_for_movie_message = '' if not is_without_image else \
                                         "<p>==>Image not found: "\
                                         "Movies must have images with imdb id as their file name</p>"\
                                         + "".join([
                                          f"<p>{movie.imdb_id}</p>"
                                          f"<p>{movie.name}</p>"
                                          for movie in movies_without_images]) + "<p>Please upload them manually!</p>"

            send_email(
                from_email='cinemaX@test.ro',
                to_email='liviu.m.farcas@gmail.com',
                subject='Your movie import statistics',
                html_content=f"Hello,"
                             "<p>Your movies have been uploaded successfully!</p>"
                             f'{no_image_for_movie_message}'
                             +
                             f'{duplicate_movie_message}'
                             '<br/><p>Have a good one!</p>'
                             '<br/> Cinema X'
            )

        form = CsvImport()
        payload = {"form": form}
        return render(
            request, "admin/zip_upload.html", payload
        )


admin.site.register(Reservation)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Cinema)
admin.site.register(ContactMessages)
admin.site.register(Hall)
admin.site.register(Schedule)
admin.site.register(Seat)
