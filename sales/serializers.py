from compat.django_rest_framework import serializers

from .models import Ticket, Order


class TicketSerializer(serializers.ModelSerializer):
    passenger = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Ticket
        exclude = ['order', 'id']


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
