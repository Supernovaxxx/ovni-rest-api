from drf_writable_nested import UniqueFieldsMixin
from rest_framework import serializers

from .models import Place


class PlaceSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = "__all__"
