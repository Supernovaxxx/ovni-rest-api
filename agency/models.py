from django.contrib.auth.models import Group, Permission
from django.db import models
from compat.django_guardian.models import GuardedModel

from event.models import Event

from .managers import TourManager, AgencyGroupQuerySet


class Agency(GuardedModel):
    title = models.CharField(max_length=50, unique=True)
    group = models.OneToOneField('auth.Group', models.PROTECT, null=True)

    class Meta:
        verbose_name_plural = "agencies"

    def __str__(self):
        return self.title


class AgencyGroup(Group):

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

    objects = AgencyGroupQuerySet.as_manager()

    class Meta:
        proxy = True
        auto_created = True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.create_default_permissions()

    def create_default_permissions(self):
        self.permissions.set(
            self._get_permissions_for_codenames_in('default_permissions')
        )

        related_fieldname = self.__kind__.lower()
        related_object = getattr(self, related_fieldname)

        for perm in self._get_permissions_for_codenames_in('default_object_permissions'):
            self.add_obj_perm(perm, related_object)

    def _get_permissions_for_codenames_in(self, attrname):
        codenames = getattr(self, attrname)
        return Permission.objects.filter(codename__in=codenames)


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
