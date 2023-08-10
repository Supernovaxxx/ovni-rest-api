import googlemaps
from django.conf import settings

GOOGLE_MAPS_API_CLIENT = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
