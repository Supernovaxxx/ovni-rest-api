import pytest
import random


@pytest.fixture()
@pytest.mark.django_db
def populate_db_with_events(event_factory, inactive_event_factory):
    def _populate(nb_active=5, nb_inactive=5, nb_events=None):
        if nb_events and type(nb_events) == int and nb_events <= 50:
            nb_active = random.randrange(1, nb_events)
            nb_inactive = nb_events - nb_active

        return (event_factory.create_batch(nb_active),
                inactive_event_factory.create_batch(nb_inactive))

    return _populate
