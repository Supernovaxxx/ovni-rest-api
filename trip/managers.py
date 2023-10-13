from django.db.models import Count

from compat.django_guardian.managers import GuardedManager


class TripManager(GuardedManager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(trip_passenger_count=Count('route__tickets__passenger'))
        )


class WaypointManager(GuardedManager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(waypoint_passenger_count=Count('tickets__passenger'))

            # TODO: Annotate a list of passenger using django.contrib.postgres.aggregates.ArrayAgg
        )
