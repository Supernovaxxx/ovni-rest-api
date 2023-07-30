import requests
import json

from drf_writable_nested import UniqueFieldsMixin
from rest_framework import serializers

from __project__.settings import GOOGLE_MAPS_API_KEY
from .models import Place


GEOCODE_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"


def _get_updated_fields_from_google_api(place_id):
    place_data = requests.get(GEOCODE_BASE_URL,
                              params={"place_id": place_id,
                                      "key": GOOGLE_MAPS_API_KEY},
                              )

    place_data = json.loads(place_data.text)["results"][0]

    formatted_address = place_data["formatted_address"]
    latitude = place_data["geometry"]["location"]["lat"]
    longitude = place_data["geometry"]["location"]["lng"]
    city = None
    state = None
    country = None

    for item in place_data["address_components"]:
        if city is None and "administrative_area_level_2" in item["types"]:
            city = item["short_name"]
        if state is None and "administrative_area_level_1" in item["types"]:
            state = item["short_name"]
        if country is None and "country" in item["types"]:
            country = item["short_name"]

    return formatted_address, latitude, longitude, city, state, country


class PlaceSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = "__all__"

    def create(self, validated_data):
        place_id = validated_data["place_id"]

        formatted_address, latitude, longitude, city, state, country = _get_updated_fields_from_google_api(place_id)

        return Place.objects.create(place_id=place_id,
                                    formatted_address=formatted_address,
                                    city=city,
                                    state=state,
                                    country=country,
                                    latitude=latitude,
                                    longitude=longitude)

    def update(self, instance, validated_data):
        if validated_data["place_id"] == instance.place_id:
            return instance
        else:
            place_id = validated_data["place_id"]

            updated_data = _get_updated_fields_from_google_api(place_id)

            for field, data in self.fields, updated_data:
                instance.field = data

            instance.save()

            return instance
