from rest_framework import serializers
from .models import Place


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = "__all__"

    def to_representation(self, place_id):
        return place_id

    def to_internal_value(self, place_id):
        place, _ = Place.objects.get_or_create_from_maps_api(place_id)
        return place
