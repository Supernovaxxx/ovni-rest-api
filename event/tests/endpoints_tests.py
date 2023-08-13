import pytest

from faker import Faker

from django.urls import reverse

from event.models import Event

fake = Faker()


@pytest.mark.django_db
def test_unauthenticated_event_list_request_is_readable(unauthenticated_api_client, create_three_active_events):
    url = reverse('events-list')
    get_response = unauthenticated_api_client.get(url)

    assert 200 == get_response.status_code
    assert 3 == get_response.data["count"]


@pytest.mark.django_db
def test_unauthenticated_event_detail_request_is_readable(unauthenticated_api_client, create_three_active_events):
    event = Event.objects.first()

    url = reverse('events-detail', kwargs={"pk": event.pk})
    get_response = unauthenticated_api_client.get(url)

    assert 200 == get_response.status_code
    assert event.pk == get_response.data["id"]


@pytest.mark.django_db
def test_unauthenticated_event_create_request(unauthenticated_api_client):
    payload = {
        "title": "A",
        "subtitle": "B",
        "start_date": fake.past_datetime(),
        "end_date": fake.future_datetime()
    }

    url = reverse('events-list')
    post_response = unauthenticated_api_client.post(url, data=payload, format="json")

    assert post_response.status_code == 403
    assert post_response.data["errors"][0]["code"] == "not_authenticated"
