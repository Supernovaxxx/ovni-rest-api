import pytest
from pytest_cases import parametrize_with_cases

from event.serializers import EventSerializer
from event.models import Event
from .test_models_cases import EventData


@parametrize_with_cases("data", cases=EventData)
@pytest.mark.django_db
def test_event_creation(data):
    """
    Test event creation and validation with different input scenarios.

    This test method uses pytest's parameterization feature to run multiple test cases
    with various combinations of input data for creating an event. It verifies that
    the EventSerializer correctly validates the input data based on the provided
    'validity' parameter.
    """

    validity = data.pop("validity")
    serializer = EventSerializer(data=data)

    return serializer.is_valid() is validity


@pytest.mark.django_db
def test_event_upcoming_manager_method(event_factory):
    """
    Test the 'active' manager method of the Event model.

    This test method populates the database with a specified number of active and
    inactive events using fixtures, and then checks if the 'active' manager method
    correctly filters and counts the active events.
    """

    nb_upcoming = 3
    nb_past = 7

    event_factory.create_batch(size=nb_upcoming, upcoming=True)
    event_factory.create_batch(size=nb_past, past=True)

    filtered_upcoming_events = Event.objects.upcoming()
    assert nb_upcoming == filtered_upcoming_events.count()

    event_factory.create_batch(size=nb_upcoming, upcoming=True)
    event_factory.create_batch(size=nb_past, past=True)

    filtered_upcoming_events = Event.objects.upcoming()
    assert nb_upcoming + nb_upcoming == filtered_upcoming_events.count()
