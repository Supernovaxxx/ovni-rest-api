from django.core.exceptions import FieldError
from rest_framework import viewsets, permissions

from .permissions import IsReadOnly


class QueryParamFilterableModelViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.DjangoObjectPermissions | IsReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()

        if params := self.request.query_params:
            qs = filter_by_query_params(qs, params)

        return qs


def filter_by_query_params(qs, params):
    filters = {}
    for param, value in params.items():
        filters[param] = value

    if filters:
        try:
            return qs.filter(**filters)
        except FieldError as e:
            raise e
