import requests

from __project__.settings import GOOGLE_MAPS_API_KEY


def get_place_data_from_geocode_api(place_id):
    geocode_data = _get_geocode_data(
        place_id=place_id,
        key=GOOGLE_MAPS_API_KEY,
    )

    ret = {
        "place_id": place_id,
        "formatted_address": geocode_data["formatted_address"],
        "latitude": geocode_data["geometry"]["location"]["lat"],
        "longitude": geocode_data["geometry"]["location"]["lng"],
    }

    for item in geocode_data["address_components"]:
        if "administrative_area_level_2" in item["types"]:
            ret["city"] = item["short_name"]

        if "administrative_area_level_1" in item["types"]:
            ret["state"] = item["short_name"]

        if "country" in item["types"]:
            ret["country"] = item["short_name"]

    return ret


def _get_geocode_data(**params):
    """Interface with Google Maps Geocode API"""
    geocode_api_url = "https://maps.googleapis.com/maps/api/geocode/json"

    try:
        response = requests.get(geocode_api_url, **params)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise ValueError(e)

    result = response.json()["results"]
    if not result:
        raise ValueError(f"The provided 'place_id' has no correspondence on Google Maps Geocode API")

    return result[0]
