from compat.django_rest_framework import serializers

from sales.serializers import TicketSerializer
from geo.serializers import PlaceSerializer
from .models import Trip, Waypoint


_TicketPassengersNestedSerializer = TicketSerializer.with_meta(fields=['passenger'])


class WaypointSerializer(serializers.ModelSerializer):
    place_id = PlaceSerializer(source='place')
    waypoint_passenger_count = serializers.IntegerField(read_only=True)
    tickets = _TicketPassengersNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Waypoint
        exclude = ['trip', 'id', 'order', 'place']

    def to_representation(self, instance):
        """Overrides Waypoint representation to include flattened Place attributes."""
        representation = super().to_representation(instance)

        place_representation = representation.pop('place_id')
        for field_name in place_representation:
            representation[field_name] = place_representation[field_name]

        return representation


class TripSerializer(serializers.WriteableNestedModelSerializer):
    route = WaypointSerializer(many=True, allow_empty=False)
    trip_passenger_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Trip
        fields = '__all__'
