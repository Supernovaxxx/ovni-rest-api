from django.contrib.auth import get_user_model
from django.db import models
from django.utils.functional import classproperty

from agency.models import Agency, AgencyRelatedModel
from trip.models import Waypoint

from .managers import TicketManager, OrderManager


User = get_user_model()


class Order(AgencyRelatedModel):
    class Types(models.TextChoices):
        PENDING = 'Pending'
        PAID = 'Paid'
        CANCELED = 'Canceled'

    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    emission_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=Types.choices, default='Pending')

    objects = OrderManager()


class Ticket(AgencyRelatedModel):
    passenger = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    waypoint = models.ForeignKey(Waypoint, on_delete=models.CASCADE, related_name='tickets')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='tickets')

    objects = TicketManager()

    @property
    def agency(self):
        return self.waypoint.trip.tour.agency

    @classproperty
    def agency_path(cls):
        return 'waypoint__trip__tour__agency'
