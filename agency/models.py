from django.db import models

from event.models import Event


class Agency(models.Model):
    title = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "agencies"


class Tour(models.Model):
    agency = models.ForeignKey(Agency, models.DO_NOTHING)
    event = models.ForeignKey(Event, models.DO_NOTHING)

    class Meta:
        ordering = ['agency']
