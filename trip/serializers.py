from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer

from .models import Trip, Waypoint


class WaypointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waypoint
        fields = "__all__"


class TripSerializer(WritableNestedModelSerializer):
    waypoints = WaypointSerializer(many=True)

    class Meta:
        model = Trip
        fields = "__all__"
