from rest_framework.decorators import api_view
from rest_framework import filters, generics
from rest_framework.response import Response

from .serializers import MovieSerializer, MovieSerializerWithSchedules, HallSerializer, ScheduleSerializer, ReservationSerializer
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


@api_view(['POST'])
def create_hall(request):
    cinema_name = request.data['cinema']
    request.data['cinema'] = Cinema.objects.filter(name=cinema_name).first().pk
    serializer = HallSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        print(f"Creating Hall Failed with following error: \n{serializer.errors}")
    return Response(serializer.data)


@api_view(['POST'])
def update_hall(request):
    hall_name = request.data['name']
    cinema_name = request.data['cinema']
    request.data['cinema'] = Cinema.objects.filter(name=cinema_name).first().pk
    hall = Hall.objects.get(name=hall_name)
    serializer = HallSerializer(instance=hall, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def create_movie(request):
    serializer = MovieSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        print(f"Creating Movie Failed with following error: \n{serializer.errors}")
    return Response(serializer.data)


@api_view(['POST'])
def update_movie(request):
    movie_name = request.data['name']
    movie_instance = Movie.objects.filter(name=movie_name).first()
    serializer = MovieSerializer(instance=movie_instance, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def create_schedule(request):
    serializer = ScheduleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        print(f"Creating Schedule Failed with following error: \n{serializer.errors}")
    return Response(serializer.data)


@api_view(['POST'])
def update_schedule(request):
    schedule = Schedule.objects.get(pk=request.data['schedule'])
    serializer = ScheduleSerializer(instance=schedule, data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        print(f"Updating Schedule Failed with following error: \n{serializer.errors}")
    return Response(serializer.data)


@api_view(['POST'])
def confirm_reservation(request):
    reservation = Reservation.objects.get(pk=request.data['reservation'])
    serializer = ReservationSerializer(instance=reservation, data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)
    return Response(serializer.data)


class MovieSearchView(generics.ListAPIView):
    search_fields = ['imdb_id', 'name']
    filter_backends = (filters.SearchFilter,)
    serializer_class = MovieSerializer

    def get_queryset(self):
        queryset = Movie.objects.all()
        imdb_id = self.request.query_params.get('imdb_id', '')
        movie_name = self.request.query_params.get('name', '')
        if imdb_id:
            return queryset.filter(imdb_id=imdb_id)
        elif movie_name:
            return queryset.filter(name=movie_name)
        return queryset


class ReservationListCreate(generics.ListCreateAPIView):
    permission_classes = [permissions.IsOwner]
    serializer_class = ReservationSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Reservation.objects.all()
        else:
            return Reservation.objects.filter(user=self.request.user)


class ReservationListUpdate(generics.UpdateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsOwner]

    def perform_update(self, serializer):
        instance = serializer.save()
