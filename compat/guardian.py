from django.db.models import QuerySet

from guardian.shortcuts import get_objects_for_user


class GuardedQuerySet(QuerySet):
    def get_objects_for_user(self, user):
        app_label = self.model._meta.app_label
        model_name = self.model.__name__.lower()
        return get_objects_for_user(user, f"{app_label}.change_{model_name}", accept_global_perms=False)
