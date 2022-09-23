from rest_framework.decorators import api_view
from rest_framework import filters, generics
from rest_framework.response import Response

from .serializers import (
    MovieSerializer,
    MovieSerializerWithSchedules,
    HallSerializer,
    ScheduleSerializer,
    ReservationSerializer
)
from cinema_project.utils import today, next_days
from base_app.models import Movie, Cinema, Hall, Reservation, Schedule
from . import permissions


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


class HallListCreateUpdate(generics.CreateAPIView, generics.UpdateAPIView):
    queryset = Hall.objects.all()
    serializer_class = HallSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save()


class MovieListCreate(generics.ListCreateAPIView, generics.UpdateAPIView):
    search_fields = ['imdb_id', 'name']
    filter_backends = (filters.SearchFilter,)
    serializer_class = MovieSerializer

    def get(self, request, *args, **kwargs):
        movies = Movie.objects.all()
        serializer = self.serializer_class(movies, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = Movie.objects.all()
        imdb_id = self.request.query_params.get('imdb_id', '')
        movie_name = self.request.query_params.get('name', '')
        if imdb_id:
            return queryset.filter(imdb_id=imdb_id)
        elif movie_name:
            return queryset.filter(name=movie_name)
        return queryset

    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save()


class ScheduleListCreateUpdate(generics.CreateAPIView, generics.UpdateAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save()


class ReservationListCreateUpdate(generics.ListCreateAPIView, generics.UpdateAPIView):
    permission_classes = [permissions.IsOwner]
    serializer_class = ReservationSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Reservation.objects.all()
        else:
            return Reservation.objects.filter(user=self.request.user)

    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save()
