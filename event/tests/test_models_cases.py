import factory

from .factories import EventFactory

from pytest_cases import case, parametrize


class EventData:
    @case(tags="valid_data")
    def case_valid_data(self):
        event_data = factory.build(dict, FACTORY_CLASS=EventFactory)
        event_data["validity"] = True
        return event_data

    @parametrize(blank_key=["title", "subtitle", "start_date", "end_date"])
    def case_blank_field_in_data(self, blank_key: str):
        data = factory.build(dict, FACTORY_CLASS=EventFactory)
        data[blank_key] = ""
        data["validity"] = True if blank_key == "subtitle" else False
        return data

    @parametrize(null_key=["title", "subtitle", "start_date", "end_date"])
    def case_null_field_in_data(self, null_key: str):
        data = factory.build(dict, FACTORY_CLASS=EventFactory)
        data[null_key] = None
        data["validity"] = True if null_key == "subtitle" else False
        return data

    @case(tags="invalid_data")
    def case_invalid_data(self):
        event_data = factory.build(dict, FACTORY_CLASS=EventFactory, invalid=True)
        event_data["validity"] = False
        return event_data
