from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class Hall(models.Model):
    name = models.CharField(max_length=200, default=None)
    description = models.TextField(max_length=400, default=None)
    seats = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Movie(models.Model):
    name = models.CharField(max_length=200, default=None)
    poster = models.ImageField(upload_to="static/media/", default=None)
    description = models.TextField(default=None)
    year = models.FloatField(default=None)
    director = models.CharField(max_length=200, default=None)
    imdb_link = models.CharField(max_length=400, default='https://imdb.com')
    imdb_id = models.FloatField(default=None)
    url = models.CharField(max_length=400, default=None)
    duration = models.IntegerField(default=None)
    hall = models.ForeignKey(Hall, null=True, on_delete=models.SET_NULL)

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
    hall = models.CharField(max_length=30, default=None)

    def __str__(self):
        return self.name


class Schedule(models.Model):
    movie = models.ForeignKey(
        Movie, default=None, on_delete=models.SET_DEFAULT)
    hall = models.ForeignKey(
        Hall, default=None, on_delete=models.SET_DEFAULT)
    schedule_time = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return f"{self.hall}__{self.schedule_time}"


class Reservation(models.Model):
    user = models.ForeignKey(
        User, default=None, on_delete=models.CASCADE
    )
    schedule = models.ForeignKey(
        Schedule, default=None, on_delete=models.CASCADE
    )


class Seat(models.Model):
    reservation = models.ForeignKey(Reservation, default=None, on_delete=models.CASCADE)
