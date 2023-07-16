from rest_framework import serializers

from .models import Trip, Waypoint


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = "__all__"


class WaypointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waypoint
        fields = "__all__"
