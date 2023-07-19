from django.db import models

from agency.models import Tour

from geo.models import Place


class Trip(models.Model):
    tour = models.ForeignKey(Tour, models.PROTECT)
    slug = models.SlugField()
    departure = models.DateTimeField()
    capacity = models.IntegerField()


class Waypoint(models.Model):
    TYPES = [
        # TODO
    ]
    trip = models.ForeignKey(Trip, models.PROTECT, related_name="waypoints")
    place = models.ForeignKey(Place, models.CASCADE)
    order = models.IntegerField(unique=True)
    type = models.CharField(max_length=50, choices=TYPES)

    class Meta:
        ordering = ["order"]