from django.db.models import Sum, Count, QuerySet

from compat.django_guardian.managers import GuardedManager


class AgencyGroupQuerySet(QuerySet):
    def create(self, agency=None):
        if agency is None:
            raise ValueError("Agency is required.")
        agency.group = super(AgencyGroupQuerySet, self).create(agency=agency, name=agency.title)
        agency.save()
        return agency.group


class TourManager(GuardedManager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(revenue=Sum('trips__route__tickets__order__value'))
            .annotate(passenger_count=Count('trips__route__tickets__passenger'))
        )
