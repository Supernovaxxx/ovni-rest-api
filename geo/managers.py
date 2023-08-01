from django.db.models import QuerySet

from .utils import consume_place_data_from_google_api


class PlaceQuerySet(QuerySet):
    def create(self, **kwargs):
        consumed_place_data = consume_place_data_from_google_api(**kwargs)
        return super().create(**{**kwargs, **consumed_place_data})
