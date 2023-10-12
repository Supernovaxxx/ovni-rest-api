from django.db import models
from django.db.models import Count


class TripManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(trip_passenger_count=Count('route__tickets__passenger'))
        )


class WaypointManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(waypoint_passenger_count=Count('tickets__passenger'))

            # TODO: Annotate a list of passenger using django.contrib.postgres.aggregates.ArrayAgg
        )
