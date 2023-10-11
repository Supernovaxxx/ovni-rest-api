from compat.django_rest_framework import serializers

from trip.serializers import TripSerializer
from .models import Agency, Tour


class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = "__all__"


_NestedTripSerializer = TripSerializer.with_meta(exclude=['tour'])


class TourSerializer(serializers.WriteableNestedModelSerializer):
    agency = serializers.PrimaryKeyRelatedField(read_only=True)
    trips = _NestedTripSerializer(many=True, allow_empty=False)

    class Meta:
        model = Tour
        fields = "__all__"
