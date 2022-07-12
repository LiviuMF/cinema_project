from django.db import models


class Hall(models.Model):
    name = models.CharField(max_length=200, default=None)
    description = models.TextField(max_length=400, default=None)
    seats = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Movie(models.Model):
    name = models.CharField(max_length=200, default=None)
    poster = models.ImageField(default=None)
    description = models.TextField(default=None)
    year = models.FloatField(default=None)
    director = models.CharField(max_length=200, default=None)
    imdb_link = models.CharField(max_length=400, default='https://imdb.com')
    imdb_id = models.FloatField(default=None)
    url = models.CharField(max_length=400, default=None)
    duration = models.FloatField(default=None)
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
