import itertools as it

from rest_framework import serializers

from .models import Trip, Waypoint


def _generate_waypoints_list(trip, waypoints):
    return [Waypoint(trip=trip, order=i, **waypoint) for (i, waypoint) in enumerate(waypoints)]


class WaypointListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        fields_to_update = self.child.fields
        updated_fields = []

        trip = self.root.instance

        # Create a list with all the data that's currently in the database
        instance_data_list = instance.all()

        # Create a list with the validated data passed in the request
        validated_data_list = _generate_waypoints_list(trip, validated_data)

        # Create a list of tuples to compare incoming data with persisted data padding to the longest with None value
        comparison_list = list(it.zip_longest(instance_data_list, validated_data_list))

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
    order = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Waypoint
        exclude = ["trip", "id"]
        list_serializer_class = WaypointListSerializer


class TripSerializer(serializers.ModelSerializer):
    route = WaypointSerializer(many=True)

    class Meta:
        model = Trip
        exclude = ["id"]

    def create(self, validated_data):
        route = validated_data.pop("route")
        trip = Trip.objects.create(**validated_data)

        bulk_list = _generate_waypoints_list(trip, route)
        Waypoint.objects.bulk_create(bulk_list)

        return trip

    def update(self, instance, validated_data):
        nested_serializer = self.fields["route"]
        nested_instance = instance.route
        nested_data = validated_data.pop("route")

        nested_serializer.update(nested_instance, nested_data)

        return super(TripSerializer, self).update(instance, validated_data)
