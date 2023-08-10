from django.db.models import QuerySet, Manager

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
    pass
