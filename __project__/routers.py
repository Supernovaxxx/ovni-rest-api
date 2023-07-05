from rest_framework import routers
from event.views import EventViewSet
from agency.views import AgencyViewSet

router = routers.DefaultRouter()
router.register('events', EventViewSet, basename='event')
router.register('agencies', AgencyViewSet, basename='agency')
