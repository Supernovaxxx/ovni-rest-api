from django.db import models

from agency.models import Tour

from geo.models import Place


class Trip(models.Model):
    tour = models.ForeignKey(Tour, models.PROTECT)
    slug = models.SlugField()
    departure = models.DateTimeField()
    capacity = models.IntegerField()


class Waypoint(models.Model):
    class Types(models.TextChoices):
        BOARDING = "Boarding"
        STOP = "Stop"
        ATTRACTIVE = "Attractive"

    trip = models.ForeignKey(Trip, models.CASCADE, related_name="route")
    place = models.ForeignKey(Place, models.PROTECT, related_name="waypoints")
    order = models.IntegerField(null=True)
    type = models.CharField(max_length=50, choices=Types.choices)
    title = models.CharField(max_length=50, null=True, blank=True)
    detail = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ["order"]
        constraints = [
            models.UniqueConstraint(fields=["trip", "order"], name="no duplicate order")
        ]
