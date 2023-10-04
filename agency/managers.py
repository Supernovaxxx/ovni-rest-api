from django.db.models import Manager
from compat.guardian import GuardedQuerySet
from django.db.models import Manager, CharField, F, Value, ExpressionWrapper, Func


class AgencyQuerySet(GuardedQuerySet):
    pass


class AgencyManager(Manager.from_queryset(AgencyQuerySet)):
    pass


class TourQuerySet(GuardedQuerySet):
    pass


class TourManager(Manager.from_queryset(TourQuerySet)):
    pass
