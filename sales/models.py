from django.contrib.auth import get_user_model
from django.db import models

from trip.models import Waypoint


User = get_user_model()


class Order(models.Model):
    class Types(models.TextChoices):
        PENDING = 'Pending'
        PAID = 'Paid'
        CANCELED = 'Canceled'

    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    emission_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=Types.choices, default='PENDING')


class Ticket(models.Model):
    passenger = models.ForeignKey(User, on_delete=models.CASCADE)
    waypoint = models.ForeignKey(Waypoint, on_delete=models.CASCADE, related_name='tickets')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
