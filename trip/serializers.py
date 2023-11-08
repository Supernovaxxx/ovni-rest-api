from compat.django_rest_framework import serializers

from agency.validators import UserCanManage
from sales.serializers import PassengerSerializer
from geo.serializers import PlaceSerializer

from .models import Trip, Waypoint


class WaypointSerializer(serializers.ModelSerializer):
    place_id = PlaceSerializer(source='place')
    passenger_count = serializers.IntegerField(read_only=True)
    passengers = PassengerSerializer(many=True, read_only=True, source='tickets.passengers')

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
    passenger_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Trip
        fields = '__all__'
        extra_kwargs = {'tour': {'validators': [UserCanManage()]}}

