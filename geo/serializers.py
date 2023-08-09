from rest_framework import serializers
from .models import Place


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = "__all__"

    def to_internal_value(self, place_id):
        """
        Expect only a place_id, from which it'll either find the equivalent existing Place on our base
        or create a new one by consuming data from Google Maps Geocode API.
        """
        place, _ = Place.objects.get_or_create_from_maps_api(place_id)
        return place
