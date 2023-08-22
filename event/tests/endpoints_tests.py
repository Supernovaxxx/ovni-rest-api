import pytest
from datetime import datetime

from django.urls import reverse
from rest_framework import status
from faker import Faker

from event.models import Event

fake = Faker()


@pytest.mark.django_db
class TestEventListView:
    def test_list_successful_read(self, client, populate_db_with_events):
        nb_events = 5
        populate_db_with_events(nb_events=nb_events)
        list_url = reverse("events-list")
        list_response = client.get(list_url)

        assert list_response.status_code == status.HTTP_200_OK
        assert list_response.json()["count"] == nb_events

    def test_create_event_as_admin(self, admin_client):
        """Test that an admin or staff user can create an event."""

        # Create a new event (POST request)
        create_data = {
            "title": "title",
            "subtitle": "subtitle",
            "start_date": fake.past_datetime(),
            "end_date": fake.future_datetime()
        }
        create_url = reverse("events-list")
        create_response = admin_client.post(create_url, create_data)

        assert create_response.status_code == status.HTTP_201_CREATED

    def test_create_event_as_unauthorized_user(self, client):
        """Test that an unauthorized user cannot create an event."""
        # Attempt to create an event as an unauthorized user (POST request)
        create_url = reverse("events-list")
        create_data = {
            "title": "title",
            "subtitle": "subtitle",
            "start_date": fake.past_datetime(),
            "end_date": fake.future_datetime()
        }
        create_response = client.post(create_url, create_data)

        assert create_response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestEventDetailView:
    """
        Test cases for the Event detail view, covering various scenarios.

        These test cases ensure that an unauthenticated user can read the details
        of an event, unauthorized access attempts are handled correctly, and that
        non-existent events return the expected 404 response.

        Attributes:
            client (DjangoTestClient): A Django test client for making HTTP requests.
            populated_db_with_events (fixture): A fixture for populating the database
                with event data.
        """
    def test_successful_read(self, client, populate_db_with_events):
        populate_db_with_events(nb_events=5)
        event = Event.objects.last()
        url = reverse("events-detail", kwargs={"pk": event.pk})

        get_response = client.get(url)
        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.data["id"] == event.pk

    def test_non_existent_event(self, client):
        non_existent_pk = 9999  # Assuming this primary key does not exist
        url = reverse("events-detail", kwargs={"pk": non_existent_pk})

        non_existent_response = client.get(url)
        assert non_existent_response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_event_as_admin(self, admin_client, populate_db_with_events):
        """
        Test that an admin or staff user can update an event.
        """
        # Create events
        populate_db_with_events(nb_events=5)
        event = Event.objects.last()

        # Update the event (PUT request)
        update_url = reverse("events-detail", kwargs={"pk": event.pk})
        update_data = {
            "title": fake.sentence(nb_words=2),
            "subtitle": fake.sentence(nb_words=5),
            "start_date": fake.past_datetime(),
            "end_date": fake.future_datetime()
        }
        date_format = "%Y-%m-%dT%H:%M:%SZ"
        update_response = admin_client.put(update_url, data=update_data, content_type='application/json')

        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.data["title"] == update_data["title"]
        assert update_response.data["subtitle"] == update_data["subtitle"]

        # Parse the date strings from the response
        parsed_start_date = datetime.strptime(update_response.data["start_date"], date_format)
        parsed_end_date = datetime.strptime(update_response.data["end_date"], date_format)

        # Compare parsed dates with the original data
        assert parsed_start_date == update_data["start_date"]
        assert parsed_end_date == update_data["end_date"]

        # Update the event (PATCH request)
        patch_data = {
            "title": fake.sentence(nb_words=2),
            "subtitle": fake.sentence(nb_words=5)
        }
        patch_response = admin_client.patch(update_url, data=patch_data, content_type='application/json')

        assert patch_response.status_code == status.HTTP_200_OK
        assert patch_response.data["title"] == patch_data["title"]
        assert patch_response.data["subtitle"] == patch_data["subtitle"]

    def test_update_event_as_unauthorized_user(self, client, populate_db_with_events):
        """
        Test that an unauthorized user cannot update an event.
        """
        # Create events
        populate_db_with_events(nb_events=5)
        event = Event.objects.last()

        # Attempt to update the event as an unauthorized user (PUT request)
        update_url = reverse("events-detail", kwargs={"pk": event.pk})
        update_data = {
            "title": fake.words(nb=2),
            "subtitle": fake.words(nb=5),
            "start_date": fake.past_datetime(),
            "end_date": fake.future_datetime()
        }
        update_response = client.put(update_url, update_data)

        assert update_response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_event_as_admin(self, admin_client, populate_db_with_events):
        """
        Test that an admin or staff user can delete an event.
        """
        # Create events
        populate_db_with_events(nb_events=5)
        event = Event.objects.last()

        # Delete the event (DELETE request)
        delete_url = reverse("events-detail", kwargs={"pk": event.pk})
        delete_response = admin_client.delete(delete_url)

        assert delete_response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_event_as_unauthorized_user(self, client, populate_db_with_events):
        """
        Test that an unauthorized user cannot delete an event.
        """
        # Create events
        populate_db_with_events(nb_events=5)
        event = Event.objects.last()

        # Attempt to delete the event as an unauthorized user (DELETE request)
        delete_url = reverse("events-detail", kwargs={"pk": event.pk})
        delete_response = client.delete(delete_url)

        assert delete_response.status_code == status.HTTP_403_FORBIDDEN
