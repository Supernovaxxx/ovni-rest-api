from django.db import models
from django.utils.functional import classproperty

from agency.models import Tour, AgencyRelatedModel
from geo.models import Place

from .managers import TripManager, WaypointManager


class Trip(AgencyRelatedModel):
    tour = models.ForeignKey(Tour, models.CASCADE, related_name="trips")
    slug = models.SlugField()
    departure = models.DateTimeField()
    capacity = models.IntegerField()

    objects = TripManager()

    def __str__(self):
        return self.slug

    @property
    def agency(self):
        return self.tour.agency

    @agency.setter
    def agency(self, agency):
        self.agency = agency

    @classproperty
    def agency_path(self):
        return 'tour__agency'


class Waypoint(AgencyRelatedModel):
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

    objects = WaypointManager()

    class Meta:
        ordering = ["trip", "order"]
        constraints = [
            models.UniqueConstraint(fields=["trip", "order"], name="no duplicate order")
        ]

    def __str__(self):
        return self.title or str(self.place)
