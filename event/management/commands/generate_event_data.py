from random import choice
from django.core.management.base import BaseCommand
from event.tests.factories import EventFactory

# Define a default quantity of events
DEFAULT_QUANTITY = 25


def _generate_random_number_of_events(quantity=DEFAULT_QUANTITY):
    extra_events = [choice([1, -1]) for _ in range(quantity)]
    upcoming = extra_events.count(1)
    past = extra_events.count(-1)
    return upcoming, past


class Command(BaseCommand):
    help = (
        "Create events with specified quantities of past and upcoming events."
        f"If quantity is not provided creates {DEFAULT_QUANTITY} events."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "quantity",
            type=int,
            nargs="?",
            help="The quantity of events to create. If not provided, it will use the default quantity.",
        )
        parser.add_argument(
            "-u",
            "--upcoming",
            type=int,
            default=0,
            help="The quantity of upcoming events to create.",
        )
        parser.add_argument(
            "-p",
            "--past",
            type=int,
            default=0,
            help="The quantity of past events to create.",
        )

    def handle(self, *args, quantity=None, upcoming=None, past=None, **options):
        # Check if a custom quantity is provided as a command-line argument
        if quantity:
            # Check if both 'past' and 'upcoming' quantities are provided
            if past and upcoming:
                total_events_passed = past + upcoming

                # Check if the total events exceed the specified quantity
                if total_events_passed > quantity:
                    raise ValueError(
                        "The sum of upcoming and/or past cannot exceed quantity."
                    )

                # Adjust the event counts to match the specified quantity
                elif total_events_passed < quantity:
                    extra_events = quantity - total_events_passed
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Adding {extra_events} additional events to meet quantity."
                        )
                    )
                    upcoming_extra, past_extra = _generate_random_number_of_events(
                        extra_events
                    )
                    upcoming += upcoming_extra
                    past += past_extra

            # If only one of 'past' or 'upcoming' is provided, calculate the other
            elif past or upcoming:
                if past:
                    if past > quantity:
                        raise ValueError(
                            "The sum of upcoming and/or past cannot exceed quantity."
                        )
                    upcoming = quantity - past
                else:
                    if upcoming > quantity:
                        raise ValueError(
                            "The sum of upcoming and/or past cannot exceed quantity."
                        )
                    past = quantity - upcoming
            # If neither 'past' nor 'upcoming' is provided, generate random values
            else:
                upcoming, past = _generate_random_number_of_events(quantity)
        else:  # If no argument is provided, generate random values using default quantity
            if not upcoming and not past:
                upcoming, past = _generate_random_number_of_events()
            quantity = past + upcoming

        # Create events based on the calculated 'upcoming' and 'past' quantities
        EventFactory.create_batch(size=upcoming, upcoming=True)
        EventFactory.create_batch(size=past, past=True)

        # Display a success message with the event counts
        self.stdout.write(
            self.style.SUCCESS(
                f"{quantity} events were created. {past} of them are in the past and {upcoming} of them are upcoming"
            )
        )
