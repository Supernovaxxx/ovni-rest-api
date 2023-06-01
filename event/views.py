from django.shortcuts import render

from .models import Event
from rest_framework import viewsets, permissions
from .serializers import EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows events to be viewed or edited.
    """
    queryset = Event.objects.all().order_by('-start_date')
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

