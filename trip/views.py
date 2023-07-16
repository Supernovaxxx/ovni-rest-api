from rest_framework import viewsets, permissions

from .models import Trip, Waypoint
from .serializers import TripSerializer, WaypointSerializer
from agency.permissions import IsReadOnly


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [permissions.DjangoObjectPermissions | IsReadOnly]


class WaypointViewSet(viewsets.ModelViewSet):
    queryset = Waypoint.objects.all()
    serializer_class = WaypointSerializer
    permission_classes = [permissions.DjangoObjectPermissions | IsReadOnly]
