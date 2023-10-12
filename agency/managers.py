from django.db import models
from django.db.models import Sum, Count


class TourManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(revenue=Sum('trips__route__tickets__order__value'))
            .annotate(tour_passenger_count=Count('trips__route__tickets__passenger'))
        )
