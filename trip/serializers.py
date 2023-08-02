import itertools as it

from rest_framework import serializers

from .models import Trip, Waypoint
from geo.models import Place
from geo.serializers import PlaceSerializer


def _generate_route_from_input_data(waypoints, trip=None):
    for i, waypoint in enumerate(waypoints):
        place_data = waypoint.pop("place")
        place_id = place_data["place_id"]

        place, _ = Place.objects.get_or_create(place_id=place_id)

        yield Waypoint(trip=trip, order=i, place=place, **waypoint)


class WaypointListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        fields_to_update = self.child.fields
        updated_fields = []

        trip = self.root.instance

        # Create a list with all the data that's currently in the database
        instance_route = instance.all()

        # Create a list with the validated data passed in the request
        incoming_route = _generate_route_from_input_data(validated_data, trip=trip)

        # Create a list of tuples to compare incoming data with persisted data padding to the longest with None value
        comparison_list = list(it.zip_longest(instance_route, incoming_route))

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
                        if field not in updated_fields:
                            updated_fields.append(field)
                update_queue.append(old_waypoint)
            # Queue objects for creation if the incoming data has more waypoints than persisted data
            elif new_waypoint:
                create_queue.append(new_waypoint)
            # Queue objects for deletion if the incoming data has fewer waypoints than persisted data
            elif old_waypoint:
                delete_queue.append(old_waypoint.pk)

        # Perform the necessary creations, updates and deletions
        Waypoint.objects.filter(pk__in=delete_queue).delete()
        Waypoint.objects.bulk_create(create_queue)
        if updated_fields:
            Waypoint.objects.bulk_update(update_queue, fields=updated_fields)


class WaypointSerializer(serializers.ModelSerializer):
    place = PlaceSerializer()

    class Meta:
        model = Waypoint
        exclude = ["trip", "id", "order"]
        list_serializer_class = WaypointListSerializer


class TripSerializer(serializers.ModelSerializer):
    route = WaypointSerializer(many=True)

    class Meta:
        model = Trip
        exclude = ["id"]

    def create(self, validated_data):
        input_route = validated_data.pop("route")
        route_waypoints = _generate_route_from_input_data(input_route)

        route = Waypoint.objects.bulk_create(route_waypoints)  # Route creation must happen before trip creation

        trip = Trip.objects.create(**validated_data)

        for waypoint in route:
            waypoint.trip = trip

        Waypoint.objects.bulk_update(route, fields=["trip"])

        return trip

    def update(self, instance, validated_data):
        nested_serializer = self.fields["route"]
        nested_instance = instance.route
        nested_data = validated_data.pop("route")

        nested_serializer.update(nested_instance, nested_data)

        return super(TripSerializer, self).update(instance, validated_data)
