from pytest_cases import case, parametrize

from .factories import random_title, random_subtitle, random_past_date, random_future_date


def create_event_data_from_key_values(blank_key=None, null_key=None):
    key_values = [
        ("title", random_title()),
        ("subtitle", random_subtitle()),
        ("start_date", random_past_date()),
        ("end_date", random_future_date()),
    ]
    if blank_key:
        data = {k: (v if k != blank_key else "")
                for (k, v)
                in key_values}
        if blank_key != "subtitle":
            data["validity"] = False
        else:
            data["validity"] = True

    elif null_key:
        data = {k: (v if k != null_key else None)
                for (k, v)
                in key_values}
        data["validity"] = False

    else:
        data = {k: v for (k, v) in key_values}
        data["validity"] = True

    return data


class EventData:
    @case(tags='valid_data')
    def case_valid_data(self):
        return create_event_data_from_key_values()

    @parametrize(blank_key=["title", "subtitle", "start_date", "end_date"])
    def case_blank_field_in_data(self, blank_key: str):
        return create_event_data_from_key_values(blank_key=blank_key)

    @parametrize(null_key=["title", "subtitle", "start_date", "end_date"])
    def case_null_field_in_data(self, null_key: str):
        return create_event_data_from_key_values(null_key=null_key)

    def case_invalid_dates_in_data(self):
        return {
            "title": random_title(),
            "subtitle": random_subtitle(),
            "start_date": random_future_date(),
            "end_date": random_past_date(),
            "validity": False
        }
