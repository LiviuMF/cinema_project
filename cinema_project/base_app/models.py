from django.db import models


class Movie(models.Model):
    name = models.CharField(max_length=200)
    poster = models.ImageField()
    description = models.TextField()
    imdb = models.FloatField()
    url = models.CharField(max_length=400)
    duration = models.FloatField()
    
