from rest_framework import viewsets, permissions

from .models import Agency, Tour
from .serializers import AgencySerializer, TourSerializer
from .permissions import IsReadOnly


class AgencyViewSet(viewsets.ModelViewSet):
    queryset = Agency.objects.all()
    serializer_class = AgencySerializer
    permission_classes = [permissions.DjangoObjectPermissions | IsReadOnly]


class TourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    permission_classes = [permissions.DjangoObjectPermissions | IsReadOnly]
