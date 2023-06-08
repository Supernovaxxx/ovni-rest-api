from django.db import models
from django.db.models import Q, F

from .managers import EventManager


class Event(models.Model):
    title = models.TextField()
    subtitle = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    objects = EventManager()

    class Meta:
        ordering = ["-start_date"]
        constraints = [
            models.CheckConstraint(
                check=Q(end_date__gt=F("start_date")),
                name="end_date_gt_start_date",
            ),
        ]
