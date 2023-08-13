import pytest
from rest_framework.test import APIClient
from .factories import EventFactory


@pytest.fixture()
def unauthenticated_api_client() -> APIClient:
    """
    Fixture to provide an API client
    :return: APIClient
    """
    yield APIClient()


@pytest.fixture
def create_three_active_events(scope="module"):
    return EventFactory(), EventFactory(), EventFactory()
