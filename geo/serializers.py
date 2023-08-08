from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

# Without UniqueFieldsMixin, trying to create a Trip with an already existing Place will result in
# "400 Bad request" error stating there's already a Place with the given place_id
from drf_writable_nested import UniqueFieldsMixin

from .models import Place
from .utils import consume_place_data_from_google_api


class PlaceSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = "__all__"

    def to_representation(self, place_id):
        return place_id

    def to_internal_value(self, place_id):
        try:
            return Place.objects.get(pk=place_id)
        except ObjectDoesNotExist:
            return self.create(consume_place_data_from_google_api(place_id))
