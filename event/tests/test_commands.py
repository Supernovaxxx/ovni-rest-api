import pytest

from django.core.management import call_command

from event.models import Event
from event.management.commands.generate_event_data import DEFAULT_QUANTITY


def call_command_and_count_events(command_name, *args, **kwargs):
    """
    Execute a Django management command and count events before and after the execution.

    Args:
        command_name (str): The name of the Django management command to execute.
        *args: Positional arguments to pass to the command.
        **kwargs: Keyword arguments to pass to the command.

    Returns:
        tuple: A tuple containing the total events added, upcoming events added, and past events added.

    """
    events_count_before_command = Event.objects.count()
    upcoming_events_count_before_command = Event.objects.upcoming().count()

    call_command(command_name, *args, **kwargs)

    events_count_after_command = Event.objects.count()
    upcoming_events_count_after_command = Event.objects.upcoming().count()

    total_events_added = events_count_after_command - events_count_before_command
    upcoming_events_added = (
        upcoming_events_count_after_command - upcoming_events_count_before_command
    )
    past_events_added = total_events_added - upcoming_events_added

    return total_events_added, upcoming_events_added, past_events_added


class TestGenerateEventDataCommand:
    """
    Test suite for the 'generate_event_data' Django management command.

    Attributes:
        command_name (str): The name of the 'generate_event_data' command.

    """

    command_name = "generate_event_data"

    @pytest.mark.parametrize(
        "expected_upcoming, expected_past",
        [
            (0, 0),
            (50, 50),
            (0, 50),
            (50, 0),
        ],
    )
    @pytest.mark.django_db
    def test_no_quantity(self, expected_upcoming, expected_past):
        """
        Test the behavior of the 'generate_event_data' command when no quantity is specified.

        Args:
            expected_upcoming (int): The expected number of upcoming events.
            expected_past (int): The expected number of past events.

        """
        if expected_upcoming or expected_past:
            (
                total_events_added,
                upcoming_events_added,
                past_events_added,
            ) = call_command_and_count_events(
                self.command_name, upcoming=expected_upcoming, past=expected_past
            )
            events_to_be_added = expected_upcoming + expected_past
            assert total_events_added == events_to_be_added
            assert upcoming_events_added == expected_upcoming
            assert past_events_added == expected_past
        else:
            total_events_added, _, _ = call_command_and_count_events(self.command_name)
            assert total_events_added == DEFAULT_QUANTITY

    @pytest.mark.parametrize(
        "expected_quantity, expected_upcoming, expected_past",
        [
            (50, 0, 0),
            (50, 50, 0),
            (50, 0, 50),
            (50, 30, 20),
            (50, 1, 1),
            (50, 999, 999),
            (50, 51, 0),
            (50, 0, 999),
            (50, 999, 1),
            (50, 1, 999),
        ],
    )
    @pytest.mark.django_db
    def test_quantity_not_none(
        self, expected_quantity, expected_upcoming, expected_past
    ):
        """
        Test the behavior of the 'generate_event_data' command when a quantity is specified.

        Args:
            expected_quantity (int): The expected total number of events to be added.
            expected_upcoming (int): The expected number of upcoming events.
            expected_past (int): The expected number of past events.

        """
        if expected_upcoming + expected_past > expected_quantity:
            with pytest.raises(
                ValueError, match="The sum of upcoming and/or past cannot exceed quantity."
            ) as exc_info:
                call_command_and_count_events(
                    self.command_name,
                    expected_quantity,
                    upcoming=expected_upcoming,
                    past=expected_past,
                )
            assert exc_info.type is ValueError
        else:
            (
                total_events_added,
                upcoming_events_added,
                past_events_added,
            ) = call_command_and_count_events(
                self.command_name,
                expected_quantity,
                upcoming=expected_upcoming,
                past=expected_past,
            )

            assert total_events_added == expected_quantity
            if expected_upcoming + expected_past == expected_quantity:
                assert upcoming_events_added == expected_upcoming
                assert past_events_added == expected_past
