from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import MovieSerializer, MovieSerializerWithSchedules
from cinema_project.utils import today, next_days
from base_app.models import Movie


@api_view(['GET'])
def currently_playing(request):
    currently_playing_movies = Movie.objects.filter(schedules__schedule_time__range=[today(), next_days(7)])
    serializer = MovieSerializer(currently_playing_movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def currently_playing_with_schedule(request):
    currently_playing_movies = Movie.objects.filter(schedules__schedule_time__range=[today(), next_days(7)])
    serializer = MovieSerializerWithSchedules(currently_playing_movies, many=True)
    return Response(serializer.data)
