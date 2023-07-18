from rest_framework import serializers
from django_countries.serializers import CountryFieldMixin

from .models import Place


class PlaceSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = "__all__"
