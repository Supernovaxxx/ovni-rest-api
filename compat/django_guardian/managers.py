from django.db.models import QuerySet, Manager
from guardian.shortcuts import get_objects_for_user


class GuardedQuerySet(QuerySet):
    def for_user(self, user, actions=('manage',)):
        if user.is_anonymous:
            return self.none()

        model_name = self.model.__name__.lower()

        return get_objects_for_user(
            user,
            perms=[
                f'{action}_{model_name}'
                for action
                in actions
            ],
            klass=self.model,
            accept_global_perms=False
        )


class GuardedManager(Manager.from_queryset(GuardedQuerySet)):
    pass
