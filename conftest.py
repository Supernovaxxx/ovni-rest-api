from pytest_factoryboy import register
from event.tests.factories import EventFactory, InactiveEventFactory
from management.tests.factories import UserFactory

register(EventFactory)
register(InactiveEventFactory)
register(UserFactory)
