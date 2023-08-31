import pytest
from datetime import datetime, timezone

from django.urls import reverse
from pytest_cases import parametrize_with_cases
from rest_framework import status
from faker import Faker

from event.models import Event
from .test_models_cases import EventData

fake = Faker()


@pytest.mark.django_db
class TestEventListView:
    def test_list_successful_read(self, client, populate_db_with_events):
        """
        Test the successful retrieval of a list of events.

        This test populates the database with a specified number of events,
        sends a GET request to the events list endpoint, and asserts that the response status code
        is 200 (OK) and that the count of events in the response matches the expected number of events.
        """

        nb_events = 5
        populate_db_with_events(nb_events=nb_events)
        list_url = reverse("events-list")
        list_response = client.get(list_url)

        assert list_response.status_code == status.HTTP_200_OK
        assert list_response.json()["count"] == nb_events

    @parametrize_with_cases("valid_data", cases=EventData, has_tag="valid_data")
    def test_create_event_as_admin(self, admin_client, valid_data):
        """
        Test that an admin or staff user can create an event.

        This test simulates the creation of a new event by sending a POST request to the events list
        endpoint with appropriate data. It asserts that the response status code is 201 (Created)
        to confirm successful event creation.
        """

        # Create a new event (POST request)
        create_data = valid_data
        create_url = reverse("events-list")
        create_response = admin_client.post(create_url, create_data)

        assert create_response.status_code == status.HTTP_201_CREATED

    @parametrize_with_cases("valid_data", cases=EventData, has_tag="valid_data")
    def test_create_event_as_unauthorized_user(self, client, valid_data):
        """
        Test that an unauthorized user cannot create an event.

        This test simulates an unauthorized user's attempt to create a new event
        by sending a POST request to the events list endpoint with appropriate data
        It asserts that the response status code is 403 (Forbidden) to confirm that
        unauthorized users are not allowed to create events.
        """

        # Attempt to create an event as an unauthorized user (POST request)
        create_url = reverse("events-list")
        create_data = valid_data
        create_response = client.post(create_url, create_data)

        assert create_response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestEventDetailView:
    """
    Test cases for the Event detail view, covering various scenarios.

    These test cases ensure that an unauthenticated user can read the details
    of an event, unauthorized access attempts are handled correctly, and that
    non-existent events return the expected 404 response.
    """

    def test_successful_read(self, client, populate_db_with_events):
        """
        Test the successful retrieval of event details.

        This test populates the database with a specified number of events, retrieves
        the details of the last event using a GET request to the events detail endpoint,
        and asserts that the response status code is 200 (OK) and that the event's ID in
        the response matches the expected event's ID.
        """

        populate_db_with_events()
        event = Event.objects.last()
        url = reverse("events-detail", kwargs={"pk": event.pk})

        get_response = client.get(url)
        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.data["id"] == event.pk

    def test_non_existent_event(self, client):
        """
        Test handling of a request for a non-existent event.

        This test sends a GET request to the events detail endpoint with a primary key
        that is assumed to not exist in the database. It asserts that the response
        status code is 404 (Not Found) to confirm that non-existent events are handled
        correctly.
        """

        non_existent_pk = 9999  # Assuming this primary key does not exist
        url = reverse("events-detail", kwargs={"pk": non_existent_pk})

        non_existent_response = client.get(url)
        assert non_existent_response.status_code == status.HTTP_404_NOT_FOUND

    @parametrize_with_cases("valid_data", cases=EventData, has_tag="valid_data")
    def test_update_event_as_admin(
        self, admin_client, populate_db_with_events, valid_data
    ):
        """
        Test that an admin or staff user can update an event.

        This test creates events in the database, retrieves the last event, and then attempts
        to update it using both PUT and PATCH requests. It verifies that the responses have
        the correct status codes (200 OK) and that the updated data matches the input data.
        """

        # Create events
        populate_db_with_events()
        event = Event.objects.last()

        # Update the event (PUT request)
        update_url = reverse("events-detail", kwargs={"pk": event.pk})
        update_data = valid_data
        update_response = admin_client.put(
            update_url, data=update_data, content_type="application/json"
        )

        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.data["title"] == update_data["title"]
        assert update_response.data["subtitle"] == update_data["subtitle"]

        # Parse the date strings from the response
        parsed_start_date = datetime.fromisoformat(
            update_response.data["start_date"]
        ).replace(tzinfo=timezone.utc)
        parsed_end_date = datetime.fromisoformat(
            update_response.data["end_date"]
        ).replace(tzinfo=timezone.utc)

        # Compare parsed dates with the original data
        assert parsed_start_date == update_data["start_date"]
        assert parsed_end_date == update_data["end_date"]

        # Update the event (PATCH request)
        patch_data = {
            "title": fake.sentence(nb_words=2),
            "subtitle": fake.sentence(nb_words=5),
        }
        patch_response = admin_client.patch(
            update_url, data=patch_data, content_type="application/json"
        )

        assert patch_response.status_code == status.HTTP_200_OK
        assert patch_response.data["title"] == patch_data["title"]
        assert patch_response.data["subtitle"] == patch_data["subtitle"]

    @parametrize_with_cases("valid_data", cases=EventData, has_tag="valid_data")
    def test_update_event_as_unauthorized_user(
        self, client, populate_db_with_events, valid_data
    ):
        """
        Test that an unauthorized user cannot update an event.

        This test creates events in the database, retrieves the last event, and then attempts
        to update it as an unauthorized user using a PUT request. It verifies that the response
        status code is 403 (Forbidden) to confirm that unauthorized users cannot update events.
        """

        # Create events
        populate_db_with_events()
        event = Event.objects.last()

        # Attempt to update the event as an unauthorized user (PUT request)
        update_url = reverse("events-detail", kwargs={"pk": event.pk})
        update_data = valid_data
        update_response = client.put(update_url, update_data)

        assert update_response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_event_as_admin(self, admin_client, populate_db_with_events):
        """
        Test that an admin or staff user can delete an event.

        This test creates events in the database, retrieves the last event, and then attempts
        to delete it using a DELETE request. It verifies that the response status code is
        204 (No Content) to confirm successful event deletion.
        """

        # Create events
        populate_db_with_events()
        event = Event.objects.last()

        # Delete the event (DELETE request)
        delete_url = reverse("events-detail", kwargs={"pk": event.pk})
        delete_response = admin_client.delete(delete_url)

        assert delete_response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_event_as_unauthorized_user(self, client, populate_db_with_events):
        """
        Test that an unauthorized user cannot delete an event.

        This test creates events in the database, retrieves the last event, and then attempts
        to delete it as an unauthorized user using a DELETE request. It verifies that the response
        status code is 403 (Forbidden) to confirm that unauthorized users cannot delete events.
        """

        # Create events
        populate_db_with_events()
        event = Event.objects.last()

        # Attempt to delete the event as an unauthorized user (DELETE request)
        delete_url = reverse("events-detail", kwargs={"pk": event.pk})
        delete_response = client.delete(delete_url)

        assert delete_response.status_code == status.HTTP_403_FORBIDDEN
