import factory
from django.contrib.auth import get_user_model
from faker import Faker


User = get_user_model()
fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    """Creates a regular active user by default."""

    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user_{n:04}")
    email = factory.lazy_attribute(lambda o: fake.email())
    password = factory.django.Password("pw")
    first_name = factory.lazy_attribute(lambda o: fake.first_name())
    last_name = factory.lazy_attribute(lambda o: fake.last_name())
    is_staff = False
    is_superuser = False
    is_active = True
