from pytest_factoryboy import register
from event.tests.factories import EventFactory
from management.tests.factories import UserFactory

register(EventFactory)
register(UserFactory)
