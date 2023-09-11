from django.db import models

from event.models import Event
from .managers import AgencyManager


class Agency(models.Model):
    title = models.CharField(max_length=50, unique=True)

    objects = AgencyManager()

    class Meta:
        verbose_name_plural = "agencies"

    def __str__(self):
        return self.title


class Tour(models.Model):
    agency = models.ForeignKey(Agency, models.PROTECT)
    event = models.ForeignKey(Event, models.PROTECT)

    class Meta:
        ordering = ["agency"]

    def __str__(self):
        return f"Tour to '{self.event}' owned by '{self.agency}'."
