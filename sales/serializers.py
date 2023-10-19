from django.contrib.auth import get_user_model

from compat.django_rest_framework import serializers

from .models import Ticket, Order


class PassengerSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name']


class TicketSerializer(serializers.ModelSerializer):
    passenger_id = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all(), source='passenger')
    passenger_info = PassengerSerializer(source='passenger', read_only=True)

    class Meta:
        model = Ticket
        exclude = ['order', 'id', 'passenger']

    def to_representation(self, instance):
        """Overrides Ticket representation to include flattened Place attributes."""
        representation = super().to_representation(instance)

        place_representation = representation.pop('passenger_info')
        for field_name in place_representation:
            representation[field_name] = place_representation[field_name]

        return representation


class OrderSerializer(serializers.WriteableNestedModelSerializer):
    tickets = TicketSerializer(many=True, allow_empty=False)
    ticket_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
