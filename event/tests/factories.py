import random
from datetime import timedelta, UTC, datetime

from compat.faker import factory, Faker
from event.models import Event


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    title = Faker("bs")
    subtitle = Faker("optional_str", ratio=0.25)
    start_date = Faker("date_time_this_month", after_now=True, tzinfo=UTC)
    end_date = factory.LazyAttribute(
        lambda o: o.start_date + timedelta(days=random.randint(1, 7))
    )

    class Params:
        upcoming = factory.Trait(
            start_date=Faker("future_datetime", tzinfo=UTC)
        )

        past = factory.Trait(
            start_date=datetime.now(tz=UTC) - timedelta(days=random.randint(8, 31))
        )

        invalid = factory.Trait(
            end_date=factory.LazyAttribute(
                lambda o: o.start_date - timedelta(days=1))
        )
