import datetime as dt
import factory

from faker import Faker

from event.models import Event

fake = Faker()


def random_title():
    return fake.sentence(nb_words=2, variable_nb_words=True)


def random_subtitle():
    return fake.sentence(nb_words=5, variable_nb_words=True)


def random_past_date():
    return fake.past_datetime(tzinfo=dt.UTC)


def random_future_date():
    return fake.future_datetime(tzinfo=dt.UTC)


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    title = random_title()
    subtitle = random_subtitle()
    start_date = random_past_date()
    end_date = random_future_date()


class InactiveEventFactory(EventFactory):
    start_date = random_past_date()
    end_date = start_date + dt.timedelta(minutes=1)
