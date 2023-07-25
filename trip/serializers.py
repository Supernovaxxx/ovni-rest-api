import itertools as it

from rest_framework import serializers

from .models import Trip, Waypoint


class WaypointListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        trip = self.root.instance

        # Create a list with all the data that's currently in the database
        instance_data_list = instance.all()

        # Create a list with the validated data passed in the request
        validated_data_list = [Waypoint(trip=trip, order=i, **waypoint) for (i, waypoint) in enumerate(validated_data)]

        # Create a list of tuples to compare incoming data with persisted data padding to the longest with None value
        comparison_list = list(it.zip_longest(instance_data_list, validated_data_list))

        create_queue = []
        delete_queue = []
        update_queue = []

        for old_waypoint, new_waypoint in comparison_list:
            # Queue objects for creation if the incoming data has more waypoints than persisted data
            if old_waypoint is None and new_waypoint:
                create_queue.append(new_waypoint)
            # Queue objects for deletion if the incoming data has fewer waypoints than persisted data
            elif new_waypoint is None and old_waypoint:
                delete_queue.append(old_waypoint.pk)
            # Queue objects for updating after comparing incoming and persisted data
            elif old_waypoint and new_waypoint:
                for field in Waypoint._meta.get_fields():
                    if getattr(old_waypoint, field.name) != getattr(new_waypoint, field.name) and field.name != "id":
                        setattr(old_waypoint, field.name, getattr(new_waypoint, field.name))
                update_queue.append(old_waypoint)

        # Perform the necessary creations, updates and deletions
        Waypoint.objects.filter(pk__in=delete_queue).delete()
        Waypoint.objects.bulk_create(create_queue)
        Waypoint.objects.bulk_update(update_queue, fields=["place", "order"])


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

        bulk_list = [Waypoint(trip=trip, order=i, **waypoint) for (i, waypoint) in enumerate(route)]
        Waypoint.objects.bulk_create(bulk_list)

        return trip

    def update(self, instance, validated_data):
        nested_serializer = self.fields["route"]
        nested_instance = instance.route
        nested_data = validated_data.pop("route")

        nested_serializer.update(nested_instance, nested_data)

        return super(TripSerializer, self).update(instance, validated_data)
