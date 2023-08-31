import random
from datetime import timedelta, UTC
import factory

from compat.faker import Faker
from event.models import Event


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    title = Faker("bs")
    subtitle = Faker("optional_str", ratio=0.25)
    start_date = Faker("past_datetime", tzinfo=UTC)
    end_date = factory.LazyAttribute(
        lambda o: o.start_date + timedelta(days=random.randint(1, 7))
    )

    class Params:
        upcoming = factory.Trait(start_date=Faker("future_datetime", tzinfo=UTC))
        past = factory.Trait(end_date=factory.LazyAttribute(
           lambda o: o.start_date + timedelta(seconds=1))
        )
