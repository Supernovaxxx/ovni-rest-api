from django.db import models
from compat.django_guardian.models import GuardedModel

from authorization.models import ModelGroup
from event.models import Event

from .managers import TourManager


class Agency(GuardedModel):
    title = models.CharField(max_length=50, unique=True)
    group = models.OneToOneField('auth.Group', models.PROTECT, null=True)

    class Meta:
        verbose_name_plural = "agencies"

    def __str__(self):
        return self.title


class AgencyGroup(ModelGroup):

    __kind__ = 'Agency'

    default_permissions = [
        "view_agency",
        "change_agency",
        "add_tour",
        "view_tour",
        "change_tour",
        "delete_tour",
        "view_event",
    ]

    default_object_permissions = [
        "view_agency",
        "change_agency",
    ]

    class Meta:
        proxy = True
        auto_created = True


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
