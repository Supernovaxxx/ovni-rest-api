import requests
import json

from __project__.settings import GOOGLE_MAPS_API_KEY


def consume_place_data_from_google_api(place_id):
    geocode_base_url = "https://maps.googleapis.com/maps/api/geocode/json"

    try:
        response = requests.get(geocode_base_url,
                                params={"place_id": kwargs["place_id"],
                                        "key": GOOGLE_MAPS_API_KEY},
                                )

        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise ValueError(e)

    try:
        place_data = json.loads(response.text)["results"][0]
    except IndexError:
        raise ValueError("The response for this 'place_id' has returned no results.")

    ret = {
        "place_id": place_id,
        "formatted_address": place_data["formatted_address"],
        "latitude": place_data["geometry"]["location"]["lat"],
        "longitude": place_data["geometry"]["location"]["lng"],
    }

    for item in place_data["address_components"]:
        if "administrative_area_level_2" in item["types"]:
            ret["city"] = item["short_name"]

        if "administrative_area_level_1" in item["types"]:
            ret["state"] = item["short_name"]

        if "country" in item["types"]:
            ret["country"] = item["short_name"]

    return ret
