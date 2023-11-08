from agency.views import AgencyRelatedModelViewSet

from .models import Trip
from .serializers import TripSerializer


class TripViewSet(AgencyRelatedModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
