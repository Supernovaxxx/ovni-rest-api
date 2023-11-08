import factory

from factory import Faker
from faker_optional import OptionalProvider


Faker.add_provider(OptionalProvider)
