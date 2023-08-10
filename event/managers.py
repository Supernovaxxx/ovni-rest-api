from django.db.models import QuerySet, Manager


class EventQuerySet(QuerySet):
    def active(self):
        return self.filter(is_active=True)


class EventManager(Manager.from_queryset(EventQuerySet)):
    pass
