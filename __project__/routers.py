from rest_framework import routers
from event.views import EventViewSet
from agency.views import AgencyViewSet, TourViewSet

router = routers.DefaultRouter()
router.register('events', EventViewSet, basename='events')
router.register('agencies', AgencyViewSet, basename='agencies')
router.register('tours', TourViewSet, basename='tours')
