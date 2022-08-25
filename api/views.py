from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import MovieSerializer
from cinema_project.utils import today, next_days
from base_app.models import Schedule, Movie


@api_view(['GET'])
def currently_playing(request):
    movies = [schedule.movie for schedule in
              Schedule.objects.filter(schedule_time__range=[today(), next_days(7)]).order_by('schedule_time')]
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def currently_playing_with_schedule(request):
    schedules = Movie.objects.all()
    serializer = MovieSerializer(schedules, many=True)
    return Response(serializer.data)
