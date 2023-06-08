from django.db import models
from django.db.models import Q, F
from django.utils import timezone

from datetime import timedelta


class ActiveEventManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(Q(start_date__gt=timezone.now()))
        

class Event(models.Model):
    title = models.TextField()
    subtitle = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    objects = models.Manager()
    active_only = ActiveEventManager()

    class Meta:
        ordering = ["-start_date"]
        constraints = [ # TODO determine actual business constraints
            models.CheckConstraint(check=Q(start_date__gt=timezone.now()+timedelta(days=1)),
                                   name="start_date_gt_one_day"),

            models.CheckConstraint(check=Q(end_date__gt=timezone.now()+timedelta(days=2)),
                                   name="end_date_gt_two_days"),

            models.CheckConstraint(check=Q(end_date__gt=(F("start_date")+timedelta(days=1))), 
                                   name="duration_at_least_one_day"),
        ]


