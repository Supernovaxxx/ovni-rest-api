from django.shortcuts import render

from .models import Event
from rest_framework import permissions, generics
from .serializers import EventSerializer


class EventList(generics.ListCreateAPIView):
    """
    API endpoint that allows events to be viewed or created.
    """
    queryset = Event.objects.all().order_by('-start_date')
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]