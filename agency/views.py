from rest_framework import viewsets, permissions

from guardian.shortcuts import get_objects_for_user

from .models import Agency, Tour
from .serializers import AgencySerializer, TourSerializer
from management.permissions import IsReadOnly


class AgencyViewSet(viewsets.ModelViewSet):
    queryset = Agency.objects.all()
    serializer_class = AgencySerializer
    permission_classes = [permissions.DjangoObjectPermissions | IsReadOnly]


class TourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    permission_classes = [permissions.DjangoObjectPermissions | IsReadOnly]

    def perform_create(self, serializer):
        user = self.request.user
        agency = get_objects_for_user(user, "change_agency", Agency.objects.all(), accept_global_perms=False)[0]
        serializer.save(agency=agency)
