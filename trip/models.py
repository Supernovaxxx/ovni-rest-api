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
        DESTINATION = "Destination"

    trip = models.ForeignKey(Trip, models.PROTECT, related_name="route", null=True)
    place = models.ForeignKey(Place, models.CASCADE)
    order = models.IntegerField(null=True)
    type = models.CharField(max_length=50, choices=Types.choices)

    class Meta:
        ordering = ["order"]
        constraints = [
            models.UniqueConstraint(fields=["trip", "order"], name="no duplicate order")
        ]
