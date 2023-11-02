from rest_framework.exceptions import PermissionDenied

from agency.views import AgencyRelatedModelViewSet

from agency.models import Tour
from agency.utils import get_agency_for_user

from .models import Trip
from .serializers import TripSerializer


class TripViewSet(AgencyRelatedModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    def perform_create(self, serializer):
        tour_id = self.request.data.get('tour')

        if tour := Tour.objects.filter(id=tour_id, agency=get_agency_for_user(self.request.user)).first():
            serializer.save(tour=tour)
        else:
            raise PermissionDenied('You do not have permission to create a Trip for this Tour.')

    def perform_update(self, serializer):
        tour_id = self.request.data.get('tour')

        if tour := Tour.objects.filter(id=tour_id, agency=get_agency_for_user(self.request.user)).first():
            serializer.save(tour=tour)
        else:
            raise PermissionDenied('You do not have permission to create a Trip for this Tour.')



