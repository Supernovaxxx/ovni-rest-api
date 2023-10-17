from django.contrib.auth import get_user_model

from compat.django_rest_framework import serializers

from .models import Ticket, Order


class PassengerSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name']


class TicketSerializer(serializers.WriteableNestedModelSerializer):
    passenger = PassengerSerializer().with_meta(fields=['id'])

    class Meta:
        model = Ticket
        exclude = ['order', 'id']


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=True)
class OrderSerializer(serializers.WriteableNestedModelSerializer):
    tickets = TicketSerializer(many=True, allow_empty=False)

    class Meta:
        model = Order
        fields = '__all__'
