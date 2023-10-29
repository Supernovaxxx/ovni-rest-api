from rest_framework import viewsets, permissions

from .models import Agency, Tour
from .serializers import AgencySerializer, TourSerializer
from authentication.permissions import IsReadOnly


class AgencyViewSet(viewsets.ModelViewSet):
    queryset = Agency.objects.all()
    serializer_class = AgencySerializer
    permission_classes = [permissions.DjangoObjectPermissions | IsReadOnly]

    def get_queryset(self):
        return Agency.objects.for_user(self.request.user)


class TourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    permission_classes = [permissions.DjangoObjectPermissions | IsReadOnly]

    def perform_create(self, serializer):
        if agency := Agency.objects.for_user(self.request.user).first():
            serializer.save(agency=agency)

        # TODO: Deal with the case when this function is called, but the user has no agency.
