from django.contrib.auth.models import Group, Permission
from django.db import models

from .managers import GroupTypeManager, ModelGroupQuerySet


if not hasattr(Group, 'kind'):
    field = models.CharField(max_length=128, default='__default__')
    Group.add_to_class('kind', field)


class GroupType(Group):

    objects = GroupTypeManager()

    class Meta:
        proxy = True
        auto_created = True
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.create_default_permissions()

    def create_default_permissions(self):
        self.permissions.set(
            self._get_permissions_for_codenames_in('default_permissions')
        )

    def _get_permissions_for_codenames_in(self, attrname):
        codenames = getattr(self, attrname)
        return Permission.objects.filter(codename__in=codenames)


class ModelGroup(GroupType):

    objects = GroupTypeManager.from_queryset(ModelGroupQuerySet)()

    class Meta:
        proxy = True
        auto_created = True

    def create_default_permissions(self):
        super().create_default_permissions()

        related_fieldname = self.__kind__.lower()
        related_object = getattr(self, related_fieldname)

        for perm in self._get_permissions_for_codenames_in('default_object_permissions'):
            self.add_obj_perm(perm, related_object)
