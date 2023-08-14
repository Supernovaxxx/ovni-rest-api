from rest_framework import viewsets, permissions

from .models import Trip
from .serializers import TripSerializer
from management.permissions import IsReadOnly


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [permissions.DjangoObjectPermissions | IsReadOnly]
