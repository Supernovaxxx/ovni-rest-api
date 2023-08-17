import googlemaps
from googlemaps.exceptions import ApiError, HTTPError
from geo.env import env, ImproperlyConfigured


class GoogleMapsApiClient:
    def __init__(self):
        if GOOGLE_MAPS_API_KEY := env("GOOGLE_MAPS_API_KEY"):
            self._client = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

    @property
    def client(self, **params):
        if not hasattr(self, "_client"):
            raise ImproperlyConfigured(
                "Missing GOOGLE_MAPS_API_KEY environment variable."
            )
        return self._client

    def geocode(self, **params):
        """Interface with Google Maps Geocode API"""
        try:
            result = self.client.geocode(**params)
            return result[0]
        except (ApiError, HTTPError) as e:
            raise e
        except Exception as e:
            raise ValueError(
                "No correspondence found on Google Maps Geocode API"
            ) from e


GOOGLE_MAPS_API_CLIENT = GoogleMapsApiClient()
