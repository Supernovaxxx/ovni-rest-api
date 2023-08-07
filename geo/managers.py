from django.db.models import QuerySet

from .utils import consume_place_data_from_google_api


class PlaceQuerySet(QuerySet):
    def create_from_maps_api(self, place_id):
        consumed_place_data = consume_place_data_from_google_api(place_id)
        return self.create(**consumed_place_data)

    def get_or_create_from_maps_api(self, place_id):
        self._for_write = True
        try:
            return self.get(place_id=place_id), False
        except self.model.DoesNotExist:
            return self.create_from_maps_api(place_id), True
