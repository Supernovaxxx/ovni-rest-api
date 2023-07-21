from rest_framework import serializers

from .models import Trip, Waypoint


class WaypointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waypoint
        exclude = ["trip", "id"]


class TripSerializer(serializers.ModelSerializer):
    route = WaypointSerializer(many=True)

    class Meta:
        model = Trip
        exclude = ["id"]

    def create(self, validated_data):
        route = validated_data.pop("route")
        trip = Trip.objects.create(**validated_data)

        bulk_list = [Waypoint(trip=trip, order=i, **waypoint) for (i, waypoint) in enumerate(route, start=1)]
        Waypoint.objects.bulk_create(bulk_list)

        return trip

    def update(self, instance, validated_data):
        instance.route.all().delete()
        instance.delete()
        return self.create(validated_data)
