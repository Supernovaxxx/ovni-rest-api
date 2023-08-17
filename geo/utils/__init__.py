from .google_maps import GOOGLE_MAPS_API_CLIENT


def get_place_data_from_geocode_api(place_id):
    geocode_data = GOOGLE_MAPS_API_CLIENT.geocode(place_id=place_id)

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
