import pytest

from django.core.management import call_command


@pytest.fixture
@pytest.mark.django_db
def populate_db_with_events():
    def _populate(*args, **kwargs):
        call_command("generate_event_data", *args, **kwargs)
    return _populate
