from django.core.exceptions import FieldError

from rest_framework import viewsets

from .models import Order
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        qs = Order.objects.all()

        if params := self.request.query_params:
            filters = {}
            for param, value in params.items():
                filters[param] = value

            if filters:
                try:
                    qs = qs.filter(**filters)
                except FieldError as e:
                    raise e

        return qs

