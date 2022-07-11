from django.db import models


class Movie(models.Model):
    name = models.CharField(max_length=200, default='')
    poster = models.ImageField(default=None)
    description = models.TextField(default='')
    year = models.FloatField(default=None)
    director = models.CharField(max_length=200, default=None)
    imdb_link = models.CharField(max_length=400, default='https://imdb.com')
    imdb_id = models.FloatField(default=None)
    url = models.CharField(max_length=400, default='')
    duration = models.FloatField(default=None)

    def __str__(self):
        return self.name
