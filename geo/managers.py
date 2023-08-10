from django.db import models
from django.db.models import QuerySet, Manager, Value, ExpressionWrapper
from django.db.models.functions import Concat

from .utils import get_place_data_from_geocode_api


class PlaceQuerySet(QuerySet):
    def create_from_maps_api(self, place_id):
        """Creates a Place instance from Google Maps Geocode API data."""
        return self.create(
            **get_place_data_from_geocode_api(place_id)
        )

    def get_or_create_from_maps_api(self, place_id):
        """Mimics get_or_create() behavior, but it consumes data from Google Maps Geocode API to perform creation."""
        self._for_write = True
        try:
            return self.get(place_id=place_id), False
        except self.model.DoesNotExist:
            return self.create_from_maps_api(place_id), True


class PlaceManager(Manager.from_queryset(PlaceQuerySet)):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                coordinate=ExpressionWrapper(
                    Concat('latitude', Value(', '), 'longitude'),
                    output_field=models.CharField()
                ),
                google_maps_url=ExpressionWrapper(
                    Concat(
                        Value('https://www.google.com/maps/search/'),
                        Value('?api=1'),
                        Value('&query='), 'country',
                        Value('&query_place_id='), 'place_id',
                    ),
                    output_field=models.CharField()
                )
            )
        )
