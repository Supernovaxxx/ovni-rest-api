from django.db.models import Sum, Count

from compat.django_guardian.managers import GuardedManager


class TourManager(GuardedManager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(revenue=Sum('trips__route__tickets__order__value'))
            .annotate(passenger_count=Count('trips__route__tickets__passenger'))
        )
