from rest_framework import viewsets, permissions

from .models import Event
from .serializers import EventSerializer
from agency.permissions import IsReadOnly


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAdminUser | IsReadOnly]
