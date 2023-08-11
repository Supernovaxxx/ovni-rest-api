from .google_maps import GOOGLE_MAPS_API_CLIENT


def get_place_data_from_geocode_api(place_id):
    geocode_data = _get_geocode_data(place_id=place_id)

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
    try:
        result = GOOGLE_MAPS_API_CLIENT.geocode(**params)
    except Exception as e:
        raise GeocodeDataNotFoundError

    if not result:
        raise GeocodeDataNotFoundError

    return result[0]


GeocodeDataNotFoundError = ValueError('No correspondence found on Google Maps Geocode API')
