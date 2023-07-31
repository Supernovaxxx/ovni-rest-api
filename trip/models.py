from django.db import models

from agency.models import Tour

from geo.models import Place


class Trip(models.Model):
    tour = models.ForeignKey(Tour, models.PROTECT)
    slug = models.SlugField(null=True, blank=True)
    departure = models.DateTimeField(null=True, blank=True)
    capacity = models.IntegerField(null=True, blank=True)


class Waypoint(models.Model):
    class Types(models.TextChoices):
        BOARDING = "Boarding"
        STOP = "Stop"
        ATTRACTIVE = "Attractive"

    trip = models.ForeignKey(Trip, models.CASCADE, related_name="route", null=True, blank=True)
    place = models.ForeignKey(Place, models.PROTECT, related_name="waypoints", null=True, blank=True)
    order = models.IntegerField(null=True)
    type = models.CharField(max_length=50, choices=Types.choices)
    title = models.TextField(max_length=50, null=True, blank=True)
    detail = models.TextField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ["order"]
        constraints = [
            models.UniqueConstraint(fields=["trip", "order"], name="no duplicate order")
        ]
