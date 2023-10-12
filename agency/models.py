from django.db import models
from compat.django_guardian.models import GuardedModel

from event.models import Event
from .managers import TourManager


class Agency(GuardedModel):
    title = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "agencies"

    def __str__(self):
        return self.title


class Tour(GuardedModel):
    agency = models.ForeignKey(Agency, models.PROTECT)
    event = models.ForeignKey(Event, models.PROTECT)

    objects = TourManager()

    @property
    def heading(self):
        return f"Tour to '{self.event}' owned by '{self.agency}'."

    class Meta:
        ordering = ["agency"]

    def __str__(self):
        return self.heading
