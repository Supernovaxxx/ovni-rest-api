import pytest

from faker import Faker
from pytest_cases import parametrize_with_cases

from event.serializers import EventSerializer
from event.models import Event

from .test_models_cases import EventData

fake = Faker()


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
