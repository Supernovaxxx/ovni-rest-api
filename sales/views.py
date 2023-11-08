from agency.views import AgencyRelatedModelViewSet

from agency.permissions import CanManageAgency

from .models import Order
from .serializers import OrderSerializer


class OrderViewSet(AgencyRelatedModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [CanManageAgency]

    def get_queryset(self):
        return super().get_queryset().for_user(self.request.user)
