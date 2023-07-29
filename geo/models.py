from django.db import models


class Place(models.Model):
    place_id = models.CharField(max_length=255, primary_key=True)
    title = models.TextField(max_length=50, null=True, blank=True)
    detail = models.TextField(max_length=255, null=True, blank=True)
    formatted_address = models.TextField(max_length=255, null=True, blank=True)
    city = models.TextField(max_length=50, null=True, blank=True)
    state = models.TextField(max_length=50, null=True, blank=True)
    country = models.TextField(max_length=50, null=True, blank=True)
    latitude = models.DecimalField(decimal_places=8, max_digits=20, null=True, blank=True)
    longitude = models.DecimalField(decimal_places=8, max_digits=20, null=True, blank=True)
