from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class Movie(models.Model):
    name = models.CharField(max_length=200, default=None)
    poster = models.ImageField(upload_to="static/media/", default=None)
    description = models.TextField(default=None)
    year = models.IntegerField(default=None)
    director = models.CharField(max_length=200, default=None)
    imdb_link = models.CharField(max_length=400, default='https://imdb.com')
    imdb_id = models.IntegerField(default=None)
    imdb_rating = models.FloatField(default=None)
    duration = models.IntegerField(default=None)

    def __str__(self):
        return self.name


class ContactMessages(models.Model):
    name = models.CharField(max_length=200, default=None)
    email = models.EmailField()
    city = models.CharField(max_length=100, default=None)
    phone = models.CharField(max_length=20, default=None)
    cinema = models.CharField(max_length=50, default=None)
    subject = models.CharField(max_length=30, default=None)
    message = models.TextField(default=None)

    def __str__(self):
        return self.name


class Cinema(models.Model):
    name = models.CharField(max_length=30, default=None)
    description = models.TextField(max_length=200, default=None)
    city = models.CharField(max_length=100, default=None)
    address = models.TextField(default=None)

    def __str__(self):
        return self.name


class Hall(models.Model):
    name = models.CharField(max_length=200, default=None)
    description = models.TextField(max_length=400, default=None)
    seats = models.IntegerField(default=0)
    cinema = models.ForeignKey(Cinema, on_delete=models.SET_DEFAULT, default=None)

    def __str__(self):
        return self.name


class Schedule(models.Model):
    movie = models.ForeignKey(
        Movie, default=None, on_delete=models.SET_DEFAULT)
    schedule_time = models.DateTimeField(default=datetime.now())
    hall = models.ForeignKey(
        Hall, on_delete=models.CASCADE, null=True
    )

    def __str__(self):
        return f"{self.movie}__{self.hall}__{self.schedule_time}"


class Seat(models.Model):
    is_taken = models.BooleanField(default=False)
    hall = models.ForeignKey(
        Hall, on_delete=models.CASCADE, null=True
    )
    position = models.IntegerField(default=None)

    def __str__(self):
        return f"{self.position}__{self.hall}"


class Reservation(models.Model):
    user = models.ForeignKey(
        User, default=None, on_delete=models.CASCADE
    )
    seat = models.OneToOneField(Seat, on_delete=models.CASCADE, default=None)
    schedule = models.ForeignKey(
        Schedule, default=None, on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user}__{self.seat}__{self.schedule}"
