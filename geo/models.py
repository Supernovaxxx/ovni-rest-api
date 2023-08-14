from django.db import models
from .managers import PlaceManager


class Place(models.Model):
    place_id = models.CharField(max_length=255, primary_key=True)
    formatted_address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    latitude = models.DecimalField(
        decimal_places=8, max_digits=20, null=True, blank=True
    )
    longitude = models.DecimalField(
        decimal_places=8, max_digits=20, null=True, blank=True
    )

    objects = PlaceManager()
