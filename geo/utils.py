import requests
import json

from __project__.settings import GOOGLE_MAPS_API_KEY


def consume_place_data_from_google_api(**kwargs):
    geocode_base_url = "https://maps.googleapis.com/maps/api/geocode/json"

    response = requests.get(geocode_base_url,
                            params={"place_id": kwargs["place_id"],
                                    "key": GOOGLE_MAPS_API_KEY},
                            )

    response.raise_for_status()

    ret = {}

    place_data = json.loads(response.text)["results"][0]

    ret["formatted_address"] = place_data["formatted_address"]
    ret["city"] = place_data["address_components"][3]["short_name"]
    ret["state"] = place_data["address_components"][4]["short_name"]
    ret["country"] = place_data["address_components"][5]["short_name"]
    ret["latitude"] = place_data["geometry"]["location"]["lat"]
    ret["longitude"] = place_data["geometry"]["location"]["lng"]

    return ret
