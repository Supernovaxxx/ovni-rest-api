from django.db.models import Count, Manager

from agency.managers import AgencyDependentManager


class TripManager(AgencyDependentManager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related('tour__agency')
            .annotate(passenger_count=Count('route__tickets__passenger'))
        )


class WaypointManager(Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(passenger_count=Count('tickets__passenger'))

            # TODO: Annotate a list of passengers using django.contrib.postgres.aggregates.ArrayAgg
        )
