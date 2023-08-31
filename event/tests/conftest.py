import pytest

from event.management.commands.generate_event_data import DEFAULT_QUANTITY
from django.core.management import call_command


@pytest.fixture
@pytest.mark.django_db
def populate_db_with_events():
    def _populate(nb_events=DEFAULT_QUANTITY, nb_upcoming=0, nb_others=0):
        call_command("generate_event_data", nb_events, upcoming=nb_upcoming, past=nb_others)
    return _populate
