import datetime as dt

import factory
from factory import fuzzy
from faker import Faker

from event.models import Event

fake = Faker()


def now():
    return dt.datetime.now(dt.UTC)


def random_past_date(weeks_range=12):
    return fuzzy.FuzzyDateTime(now() - dt.timedelta(weeks=weeks_range)).fuzz()


def random_future_date():
    return fuzzy.FuzzyDateTime(now(), now() + dt.timedelta(days=7)).fuzz()


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    title = factory.Sequence(lambda n: f"event_{n:04}")
    subtitle = fake.sentence(nb_words=5, variable_nb_words=True)
    start_date = random_past_date()
    end_date = random_future_date()


class InactiveEventFactory(EventFactory):
    start_date = random_past_date()
    end_date = start_date + dt.timedelta(minutes=1)
