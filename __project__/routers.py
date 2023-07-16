from rest_framework import routers
from event.views import EventViewSet
from agency.views import AgencyViewSet, TourViewSet
from trip.views import TripViewSet, WaypointViewSet
from geo.views import PlaceViewSet

router = routers.DefaultRouter()
router.register('events', EventViewSet, basename='events')
router.register('agencies', AgencyViewSet, basename='agencies')
router.register('tours', TourViewSet, basename='tours')
router.register('trips', TripViewSet, basename='trips')
router.register('waypoints', WaypointViewSet, basename='waypoints')
router.register('places', PlaceViewSet, basename='places')