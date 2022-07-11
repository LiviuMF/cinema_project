from django.db import models


class Movie(models.Model):
    name = models.CharField(max_length=200)
    poster = models.ImageField()
    description = models.TextField()
    year = models.FloatField()
    director = models.CharField(200)
    imdb_link = models.CharField(max_length=400)
    imdb_id = models.FloatField()
    url = models.CharField(max_length=400)
    duration = models.FloatField()

    def __str__(self):
        return self.name
