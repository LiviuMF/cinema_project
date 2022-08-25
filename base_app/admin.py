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
            existing_movie_ids = Movie.objects.all().values_list('imdb_id', flat=True)

            movies_to_upload = []
            duplicate_movies = []
            for movie in movies_from_csv:
                if movie['imdb_id'] not in existing_movie_ids:
                    movies_to_upload.append(movie)
                else:
                    duplicate_movies.append(movie)

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

            duplicate_movies_imdb_id = [movie['imdb_id'] for movie in duplicate_movies]
            duplicate_movies_objects = Movie.objects.filter(imdb_id__in=duplicate_movies_imdb_id)
            for duplicate_movie in duplicate_movies_objects:
                for duplicate_movie_from_csv in duplicate_movies:
                    if duplicate_movie.imdb_id == duplicate_movie_from_csv['imdb_id']:
                        duplicate_movie.name = duplicate_movie_from_csv['name']
                        duplicate_movie.poster_url = duplicate_movie_from_csv['poster_image']
                        duplicate_movie.poster_image = duplicate_movie_from_csv['imdb_id'],
                        duplicate_movie.description = duplicate_movie_from_csv['description']
                        duplicate_movie.year = duplicate_movie_from_csv['year']
                        duplicate_movie.director = duplicate_movie_from_csv['director']
                        duplicate_movie.imdb_link = duplicate_movie_from_csv['imdb_link']
                        duplicate_movie.imdb_id = duplicate_movie_from_csv['imdb_id']
                        duplicate_movie.imdb_rating = duplicate_movie_from_csv['imdb_rating']
                        duplicate_movie.duration = duplicate_movie_from_csv['duration']
                        duplicate_movie.trailer_id = duplicate_movie_from_csv['trailer_id']
            Movie.objects.bulk_update(duplicate_movies_objects,
                                      ['name', 'poster_url', 'poster_image', 'description', 'year', 'director',
                                       'imdb_link', 'imdb_id', 'imdb_rating', 'duration', 'trailer_id'])

            is_duplicates = len(duplicate_movies) > 0
            movie_upload_finished_message = '' if not is_duplicates else \
                "<p>==>Movie already in db: " \
                "Movies that have not been updated as they are already in db</p>" \
                "<br/>" \
                + ",".join([movie['name'] for movie in duplicate_movies])

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
                existing_movie_ids = Movie.objects.all().values_list('imdb_id', flat=True)

                movies_to_upload = []
                duplicate_movies = []
                for movie in movies_from_csv:
                    if movie['imdb_id'] not in existing_movie_ids:
                        movies_to_upload.append(movie)
                    else:
                        duplicate_movies.append(movie)

                # fetch images from zip file
                image_types = ['.png', 'jpg', '.jpeg']
                imdb_id_and_image = {}
                for file in _zip.infolist():
                    imdb_id = os.path.basename(file.filename).split('.')[0]
                    if any(image_type in file.filename for image_type in image_types):
                        imdb_id_and_image[imdb_id] = ImageFile(_zip.open(file))
                    else:
                        imdb_id_and_image[imdb_id] = '/images/default_poster.jpg'
                    # make sure images are saved in root and not directory structure from zip
                    file.filename = os.path.basename(file.filename)

                # create new movies
                Movie.objects.bulk_create([
                    Movie(
                        name=row['name'],
                        poster_url=row['imdb_link'],
                        poster_image=imdb_id_and_image.get(row['imdb_id'], '/images/default_poster.jpg'),
                        description=row['description'],
                        year=row['year'],
                        director=row['director'],
                        imdb_link=row['imdb_link'],
                        imdb_id=row['imdb_id'],
                        imdb_rating=row['imdb_rating'],
                        duration=row['duration'],
                        trailer_id=row['trailer_id'],
                    ) for row in movies_to_upload])

                duplicate_movies_imdb_id = [movie['imdb_id'] for movie in duplicate_movies]
                duplicate_movies_objects = Movie.objects.filter(imdb_id__in=duplicate_movies_imdb_id)
                for duplicate_movie in duplicate_movies_objects:
                    for duplicate_movie_from_csv in duplicate_movies:
                        if duplicate_movie.imdb_id == duplicate_movie_from_csv['imdb_id']:
                            duplicate_movie.name = duplicate_movie_from_csv['name']
                            duplicate_movie.poster_url = duplicate_movie_from_csv['imdb_link']
                            duplicate_movie.poster_image = imdb_id_and_image.get(duplicate_movie_from_csv['imdb_id'],
                                                                                 '/images/default_poster.jpg')
                            duplicate_movie.description = duplicate_movie_from_csv['description']
                            duplicate_movie.year = duplicate_movie_from_csv['year']
                            duplicate_movie.director = duplicate_movie_from_csv['director']
                            duplicate_movie.imdb_link = duplicate_movie_from_csv['imdb_link']
                            duplicate_movie.imdb_id = duplicate_movie_from_csv['imdb_id']
                            duplicate_movie.imdb_rating = duplicate_movie_from_csv['imdb_rating']
                            duplicate_movie.duration = duplicate_movie_from_csv['duration']
                            duplicate_movie.trailer_id = duplicate_movie_from_csv['trailer_id']
                Movie.objects.bulk_update(duplicate_movies_objects,
                                          ['name', 'poster_url', 'poster_image', 'description', 'year', 'director',
                                           'imdb_link', 'imdb_id', 'imdb_rating', 'duration', 'trailer_id'])

            # notify user of import results
            movies_without_images = Movie.objects.filter(poster_image='/images/default_poster.jpg')
            is_duplicates = len(duplicate_movies) > 0
            is_without_image = len(movies_without_images) > 0

            duplicate_movie_message = '' if not is_duplicates else \
                                      "<p>==>Movie already in db: "\
                                      "Movies that have been updated in db</p>"\
                                      "<br/>"\
                                      + ",".join([movie['name'] for movie in duplicate_movies])
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
