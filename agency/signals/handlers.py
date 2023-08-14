import itertools

from django.contrib.auth.models import Group, Permission
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver

from guardian.shortcuts import assign_perm, get_groups_with_perms

from ..models import Agency, Tour


@receiver(post_save, sender=Agency)
def set_permissions(sender, instance, created, **kwargs):
    """
    When an Agency is created, this signal will create a managers group for it and
    assign the managers permission to edit the Agency and create Tours.
    """

    if created:
        group = Group.objects.create(name=f"{instance.title} Managers")

        perms = Permission.objects.filter(
            Q(codename__contains="agency") | Q(codename__contains="tour")
        )

        manager_perms = [
            i
            for i in perms
            if i.codename
            in [
                "view_agency",
                "change_agency",
                "add_tour",
                "view_tour",
                "change_tour",
                "delete_tour",
            ]
        ]

        group.permissions.add(*manager_perms)

        for perm in ["view_agency", "change_agency"]:
            assign_perm(perm, group, instance)


@receiver(post_save, sender=Tour)
def set_permissions(sender, instance, created, **kwargs):
    """
    When a new Tour is created, this signal will retrieve the associated manager group for it and
    assign the appropriate object level permissions for the Tour.
    """

    if created:
        groups = get_groups_with_perms(instance.agency)
        perms = ["view_tour", "change_tour", "delete_tour"]

        groups_and_perms = itertools.product(groups, perms)

        for group, perm in groups_and_perms:
            assign_perm(perm, group, instance)
