from django.db.models import QuerySet, Manager
from guardian.shortcuts import get_objects_for_user


class AgencyQuerySet(QuerySet):
    def get_objects_for_user(self, user):
        return get_objects_for_user(user, "agency.change_agency", accept_global_perms=False)


class AgencyManager(Manager.from_queryset(AgencyQuerySet)):
    pass
