from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver

from guardian.shortcuts import assign_perm

from ..models import Agency


@receiver(post_save, sender=Agency)
def set_permissions(sender, instance, created, **kwargs):
    """
    When a new agency is created, this signal will create a managers group for it and
    assign the managers permission to edit the agency.
    """
    view = f"view_{instance._meta.model_name}"
    change = f"change_{instance._meta.model_name}"

    if created:
        group = Group.objects.create(name=f'{instance.title} Managers')

        all_perms = Permission.objects.filter(codename__contains="agency")
        manager_perms = [i for i in all_perms if i.codename in [view, change]]

        group.permissions.add(*manager_perms)
        
        for perm in [view, change]:
            assign_perm(perm, group, instance)