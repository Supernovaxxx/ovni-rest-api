from rest_framework.exceptions import PermissionDenied

from compat.django_rest_framework.views import QueryParamFilterableModelViewSet

from .models import Agency, Tour
from .serializers import AgencySerializer, TourSerializer
from .permissions import CanManageAgency
from .utils import get_agency_for_user


class AgencyRelatedModelViewSet(QueryParamFilterableModelViewSet):
    permission_classes = [CanManageAgency]
    get_is_private = False

    def perform_create(self, serializer):
        if user_agency := get_agency_for_user(self.request.user):
            serializer.save(agency=user_agency)
        else:
            raise PermissionDenied("You're not a team member of any Agency.")

    def perform_update(self, serializer):
        if user_agency := get_agency_for_user(self.request.user):
            serializer.save(agency=user_agency)
        else:
            raise PermissionDenied("You're not a team member of any Agency.")

    def perform_destroy(self, instance):
        if user_agency := get_agency_for_user(self.request.user):

            if instance.agency == user_agency:
                instance.delete()
            else:
                raise PermissionDenied("The resource you're trying to delete does not belong to your Agency")

        else:
            raise PermissionDenied("You're not a team member of any Agency.")


class PrivateAgencyRelatedModelViewSet(AgencyRelatedModelViewSet):
    get_is_private = True


class AgencyViewSet(QueryParamFilterableModelViewSet):
    queryset = Agency.objects.all()
    serializer_class = AgencySerializer


class TourViewSet(AgencyRelatedModelViewSet):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer


