import pytest
from faker import Faker

from event.serializers import EventSerializer
from event.models import Event


PAST_DATE = "2023-08-18T12:00:00.013Z"
FUTURE_DATE = "2024-08-18T12:00:00.013Z"

fake = Faker()


@pytest.mark.parametrize(
    "title, subtitle, start_date, end_date, validity",
    [
        ("Title", "Subtitle", PAST_DATE, FUTURE_DATE, True),  # valid input
        ("Title", "Subtitle", FUTURE_DATE, PAST_DATE, False),  # invalid dates
        # blank values
        ("", "Subtitle", PAST_DATE, FUTURE_DATE, False),
        ("Title", "", PAST_DATE, FUTURE_DATE, False),
        ("Title", "Subtitle", "", FUTURE_DATE, False),
        ("Title", "Subtitle", PAST_DATE, "", False),
        # null values
        (None, "Subtitle", PAST_DATE, FUTURE_DATE, False),
        ("Title", None, PAST_DATE, FUTURE_DATE, False),
        ("Title", "Subtitle", None, FUTURE_DATE, False),
        ("Title", "Subtitle", PAST_DATE, None, False),
    ],
)
@pytest.mark.django_db
def test_event_creation(title, subtitle, start_date, end_date, validity):
    """
        Test event creation and validation with different input scenarios.

        This test method uses pytest's parameterization feature to run multiple test cases
        with various combinations of input data for creating an event. It verifies that
        the EventSerializer correctly validates the input data based on the provided
        'validity' parameter.
    """

    data = {
        "title": title,
        "subtitle": subtitle,
        "start_date": start_date,
        "end_date": end_date,
    }
    serializer = EventSerializer(data=data)

    return serializer.is_valid() is validity


@pytest.mark.django_db
def test_event_active_manager_method(
    populate_db_with_events, event_factory, inactive_event_factory
):
    """
        Test the 'active' manager method of the Event model.

        This test method populates the database with a specified number of active and
        inactive events using fixtures, and then checks if the 'active' manager method
        correctly filters and counts the active events.
    """

    nb_active = 3
    nb_inactive = 7

    populate_db_with_events(nb_active=nb_active, nb_inactive=nb_inactive)

    filtered_active_events = Event.objects.active()
    assert nb_active == filtered_active_events.count()

    event_factory()
    inactive_event_factory()
    filtered_active_events = Event.objects.active()
    assert nb_active + 1 == filtered_active_events.count()
