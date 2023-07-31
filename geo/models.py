import requests
import json

from django.db import models

from __project__.settings import GOOGLE_MAPS_API_KEY


GEOCODE_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"


class Place(models.Model):
    place_id = models.CharField(max_length=255, primary_key=True)
    formatted_address = models.TextField(max_length=255, null=True, blank=True)
    city = models.TextField(max_length=50, null=True, blank=True)
    state = models.TextField(max_length=50, null=True, blank=True)
    country = models.TextField(max_length=50, null=True, blank=True)
    latitude = models.DecimalField(decimal_places=8, max_digits=20, null=True, blank=True)
    longitude = models.DecimalField(decimal_places=8, max_digits=20, null=True, blank=True)

    def save(self, *args, **kwargs):
        place_data = requests.get(GEOCODE_BASE_URL,
                                  params={"place_id": self.place_id,
                                          "key": GOOGLE_MAPS_API_KEY},
                                  )

        place_data = json.loads(place_data.text)["results"][0]

        self.formatted_address = place_data["formatted_address"]
        self.latitude = place_data["geometry"]["location"]["lat"]
        self.longitude = place_data["geometry"]["location"]["lng"]

        for item in place_data["address_components"]:
            if "administrative_area_level_2" in item["types"]:
                self.city = item["short_name"]

            if "administrative_area_level_1" in item["types"]:
                self.state = item["short_name"]

            if "country" in item["types"]:
                self.country = item["short_name"]

        super(Place, self).save(*args, **kwargs)
