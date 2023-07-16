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
    trip = models.ForeignKey(Trip, models.DO_NOTHING)
    place = models.ForeignKey(Place, models.DO_NOTHING)
    order = models.IntegerField()
    type = models.CharField(max_length=50, choices=TYPES)
