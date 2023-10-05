from django.db.models import QuerySet, Manager
from guardian.shortcuts import get_objects_for_user


class GuardedQuerySet(QuerySet):
    def for_user(self, user):
        if user.is_anonymous:
            return self.none()

        app_label = self.model._meta.app_label
        model_name = self.model.__name__.lower()

        return get_objects_for_user(
            user,
            f"{app_label}.change_{model_name}",
            klass=self.model,
            accept_global_perms=False
        )


class GuardedManager(Manager.from_queryset(GuardedQuerySet)):
    pass
