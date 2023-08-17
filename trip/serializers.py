import itertools as it

from rest_framework import serializers

from geo.serializers import PlaceSerializer
from .models import Trip, Waypoint


class WaypointListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        """Bulk-creates several Waypoints from incoming route."""
        return Waypoint.objects.bulk_create(
            _generate_waypoints_from_incoming_route(validated_data)
        )

    def update(self, waypoints_queryset, validated_data):
        """
        Manages creations, updates and deletions of several Waypoints,
        by comparing the incoming data with the persisted one.
        """

        fields_to_update = self.child.fields
        updated_fields = set()

        # Create a list with all the data that's currently in the database
        persisted_route = waypoints_queryset.all()

        # Create a list of Waypoint instances from incoming validated data
        incoming_route = _generate_waypoints_from_incoming_route(validated_data)

        # Create a list of tuples, zipping incoming data with persisted one
        # and filling the gaps with None values
        comparison_list = list(it.zip_longest(persisted_route, incoming_route))

        create_queue = []
        delete_queue = []
        update_queue = []

        for old_waypoint, new_waypoint in comparison_list:
            # Queue objects for updating after comparing incoming and persisted data
            if old_waypoint and new_waypoint:
                for field in fields_to_update:
                    old_value = getattr(old_waypoint, field)
                    new_value = getattr(new_waypoint, field)
                    if old_value != new_value:
                        # Update old values and register the field that has been updated
                        setattr(old_waypoint, field, new_value)
                        updated_fields.add(field)
                update_queue.append(old_waypoint)
            # Queue objects for creation if the incoming data has more waypoints than persisted data
            elif new_waypoint:
                create_queue.append(new_waypoint)
            # Queue objects for deletion if the incoming data has fewer waypoints than persisted data
            elif old_waypoint:
                delete_queue.append(old_waypoint.pk)

        # Perform the necessary creations, updates and deletions
        Waypoint.objects.filter(pk__in=delete_queue).delete()
        updated_route = Waypoint.objects.bulk_create(create_queue)
        if updated_fields:
            Waypoint.objects.bulk_update(update_queue, fields=updated_fields)
            updated_route += update_queue

        return updated_route


class WaypointSerializer(serializers.ModelSerializer):
    place_id = PlaceSerializer(source="place")

    class Meta:
        model = Waypoint
        exclude = ["trip", "id", "order", "place"]
        list_serializer_class = WaypointListSerializer

    def to_representation(self, instance):
        """Overrides Waypoint representation to include flattened Place attributes."""
        representation = super().to_representation(instance)

        place_representation = representation.pop("place_id")
        for field_name in place_representation:
            representation[field_name] = place_representation[field_name]

        return representation


def _generate_waypoints_from_incoming_route(validated_data):
    for i, waypoint in enumerate(validated_data):
        yield Waypoint(order=i, **waypoint)


class TripSerializer(serializers.ModelSerializer):
    route = WaypointSerializer(many=True, min_length=1)

    class Meta:
        model = Trip
        fields = "__all__"

    @property
    def waypoint_list_serializer(self):
        return self.fields["route"]

    def create(self, validated_data):
        """Delegates route creation to specialized nested WaypointListSerializer."""

        incoming_route = validated_data.pop("route")
        trip = super(TripSerializer, self).create(validated_data)

        # Set up relation between each future new waypoint with newly created trip since
        # 'trip_waypoint.trip_id' can't be null when we create the waypoints.
        for waypoint in incoming_route:
            waypoint["trip_id"] = trip.id

        try:
            created_route = self.waypoint_list_serializer.create(incoming_route)
        except Exception as e:
            trip.delete()
            raise e

        trip.route.set(created_route)
        return trip

    def update(self, trip, validated_data):
        """Delegates route update to specialized nested WaypointListSerializer."""

        incoming_route = validated_data.pop("route", None)
        trip = super(TripSerializer, self).update(trip, validated_data)

        if incoming_route:
            persisted_route = trip.route
            updated_route = self.waypoint_list_serializer.update(
                persisted_route, incoming_route
            )
            trip.route.set(updated_route)

        return trip
