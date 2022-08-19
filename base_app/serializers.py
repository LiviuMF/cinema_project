from .models import Schedule

from rest_framework import serializers


class MovieSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Schedule
        fields = ['movie', 'schedule_time', 'hall']
