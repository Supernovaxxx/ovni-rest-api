from rest_framework import viewsets, permissions

from .models import Event
from .serializers import EventSerializer
from management.permissions import IsReadOnly


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAdminUser | IsReadOnly]
