from rest_framework import serializers

from .models import Trip, Waypoint


class WaypointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waypoint
        fields = "__all__"


class TripSerializer(serializers.ModelSerializer):
    waypoints = WaypointSerializer(many=True)

    class Meta:
        model = Trip
        fields = "__all__"

    def create(self, validated_data):
        waypoints = validated_data.pop("waypoints")
        trip = Trip.objects.create(**validated_data)
        Waypoint.objects.bulk_create(waypoints)
        return trip
