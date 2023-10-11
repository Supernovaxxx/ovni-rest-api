from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer

from trip.serializers import TripSerializer
from .models import Agency, Tour


class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = "__all__"


class TourSerializer(WritableNestedModelSerializer):
    agency = serializers.PrimaryKeyRelatedField(read_only=True)
    trips = type(
        'TripSerializer',
        (TripSerializer,),
        {
            'Meta': type('Meta', (), {
                'model': TripSerializer.Meta.model, 'exclude': ['tour']
            })
        },
    )(many=True, allow_empty=False)

    class Meta:
        model = Tour
        fields = "__all__"
