from django.db.models.signals import post_save
from django.dispatch import receiver

from ..models import Agency, AgencyGroup, Tour


@receiver(post_save, sender=Agency)
def set_permissions(sender, instance, created, **kwargs):
    """
    When an `Agency` is created, this signal will create its related `auth.Group`
    and assign the agency-type group default permissions to it.
    """

    if created:
        AgencyGroup.objects.create(agency=instance)


@receiver(post_save, sender=Tour)
def set_permissions(sender, instance, created, **kwargs):
    """
    When a new `Tour` is created, this signal will retrieve the related `AgencyGroup`
    and assign the appropriate object level permissions to it.
    """

    if created:
        for perm in ["view_tour", "change_tour", "delete_tour"]:
            instance.agency.group.add_obj_perm(perm, instance)
