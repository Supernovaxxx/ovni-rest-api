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
    - Event's shouldn't be allowed to be created with an end_date in the past of start_date.
    - All fields must be filled with valid data.
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
    populated_db_with_events, event_factory, inactive_event_factory
):
    """The active() Event queryset method should only return active events."""

    nb_active = 3
    nb_inactive = 7

    populated_db_with_events(nb_active=nb_active, nb_inactive=nb_inactive)

    filtered_active_events = Event.objects.active()
    assert 3 == filtered_active_events.count()

    event_factory()
    inactive_event_factory()
    filtered_active_events = Event.objects.active()
    assert 4 == filtered_active_events.count()
