from rest_framework import serializers
from base_app.models import Movie, Schedule


class ScheduleChildForMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    schedules = ScheduleChildForMovieSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'
