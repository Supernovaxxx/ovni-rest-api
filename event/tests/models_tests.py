import pytest

from faker import Faker
from datetime import timedelta

from event.models import Event
from .factories import EventFactory


fake = Faker()


@pytest.mark.xfail
@pytest.mark.django_db
def test_event_check_constraint():
    """
    Event's shouldn't be allowed to be created with an end_date in the past of start_date.
    """

    return Event.objects.create(
        title="A",
        subtitle="B",
        start_date=fake.future_datetime(tzinfo=fake.pytimezone()),
        end_date=fake.past_datetime(tzinfo=fake.pytimezone())
    )


@pytest.mark.django_db
def test_event_active_manager_method(create_three_active_events):
    """
    The active() Event queryset method should only return active events.
    """

    active_event = Event.objects.first()

    # Create an inactive event
    start_date = fake.past_datetime(tzinfo=fake.pytimezone())
    end_date = start_date + timedelta(hours=1)
    inactive_event = EventFactory(
        start_date=start_date,
        end_date=end_date
    )

    active_events = Event.objects.active()

    assert inactive_event not in active_events
    assert active_event in active_events


@pytest.mark.django_db
def test_events_list_ordering(create_three_active_events):
    """
    Events list should be ordered by start_date, from newest to oldest.
    """

    all_events = Event.objects.all()
    for i, current_event in enumerate(all_events):
        if i < len(all_events)-1:
            next_event = all_events[i+1]
            assert current_event.start_date > next_event.start_date
