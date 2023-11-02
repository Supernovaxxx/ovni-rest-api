from django.db import models
from compat.django_guardian.models import GuardedModel

from event.models import Event
from .managers import TourManager
    def user_can_manage(self, user):
        return user.has_perm('manage_agency', self.agency)


class Agency(GuardedModel):
    title = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = 'agencies'
        permissions = [('manage_agency', 'Can manage agency')]  # TODO: Define this in a global const

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
