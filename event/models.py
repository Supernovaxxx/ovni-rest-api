from django.db import models
from django.db.models import Q, F
from django.utils import timezone

from datetime import timedelta


class Event(models.Model):
    title = models.TextField()
    subtitle = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    objects = models.Manager()

    class Meta:
        ordering = ["-start_date"]
        constraints = [
            models.CheckConstraint(
                check=Q(end_date__gt=(F("start_date") + timedelta(days=1))),
                name="duration_at_least_one_day",
            ),
        ]



