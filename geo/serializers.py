from rest_framework import serializers

# Without UniqueFieldsMixin, trying to create a Trip with an already existing Place will result in
# "400 Bad request" error stating there's already a Place with the given place_id
from drf_writable_nested import UniqueFieldsMixin

from .models import Place


class PlaceSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = "__all__"
