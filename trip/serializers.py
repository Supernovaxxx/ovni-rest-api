import itertools as it

from rest_framework import serializers

from .models import Trip, Waypoint


class WaypointListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        trip = self.root.instance

        # Create a list with all the data that's currently in the database
        instance_data_list = [waypoint
                              for waypoint
                              in instance.all()]

        # Create a list with the validated data passed in the request
        validated_data_list = [Waypoint(trip=trip, order=i, **waypoint)
                               for (i, waypoint)
                               in enumerate(validated_data)]

        # Create a list of tuples to compare incoming data with persisted data padding to the longest with None value
        comparison_list = list(it.zip_longest(instance_data_list, validated_data_list))

        # Queue objects for creation if the incoming data has more waypoints than persisted data
        bulk_create_list = [new_waypoint
                            for (old_waypoint, new_waypoint)
                            in comparison_list
                            if old_waypoint is None and new_waypoint]

        # Queue objects for deletion if the incoming data has fewer waypoints than persisted data
        bulk_delete_list = [old_waypoint
                            for (old_waypoint, new_waypoint)
                            in comparison_list
                            if new_waypoint is None and old_waypoint]

        # Map the objects that need updating if they are different and exist in incoming and persisted data
        bulk_update_dict = {old_waypoint: new_waypoint
                            for old_waypoint, new_waypoint
                            in comparison_list
                            if old_waypoint and new_waypoint and old_waypoint != new_waypoint}

        bulk_update_list = []

        for old_waypoint, new_waypoint in bulk_update_dict.items():
            old_waypoint.order = new_waypoint.order
            old_waypoint.place = new_waypoint.place
            bulk_update_list.append(old_waypoint)

        # Perform the necessary creation, updates and deletions
        Waypoint.objects.filter(pk__in=[waypoint.pk for waypoint in bulk_delete_list]).delete()
        Waypoint.objects.bulk_create(bulk_create_list)
        Waypoint.objects.bulk_update(bulk_update_list, fields=["order", "place"])


class WaypointSerializer(serializers.ModelSerializer):
    order = serializers.IntegerField(read_only=True)

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