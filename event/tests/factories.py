import factory

from factory import fuzzy
from faker import Faker
from datetime import datetime, timedelta, timezone

from django.contrib.auth import get_user_model

from event.models import Event

User = get_user_model()
fake = Faker()
now = datetime.now(timezone.utc)


class EventFactory(factory.django.DjangoModelFactory):
    """
    Creates an active event by default.
    """
    class Meta:
        model = Event

    title = factory.Sequence(lambda n: f"event_{n:04}")
    subtitle = fake.sentence(nb_words=10, variable_nb_words=True)
    start_date = fuzzy.FuzzyDateTime(datetime(2023, 1, 1, tzinfo=timezone.utc))
    end_date = fuzzy.FuzzyDateTime(now, now + timedelta(days=7))


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user_{n:04}")
    email = factory.LazyAttribute(lambda user: f"{user.username}@test.com")
    password = factory.django.Password("pw")
