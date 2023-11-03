from agency.views import PrivateAgencyRelatedModelViewSet

from .models import Order
from .serializers import OrderSerializer


class OrderViewSet(PrivateAgencyRelatedModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        return super().get_queryset().for_user(self.request.user)
