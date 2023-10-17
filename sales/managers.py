from django.db.models import QuerySet, Manager, Count

from compat.django_guardian.managers import GuardedManager


class TicketQueryset(QuerySet):
    def passengers(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        return User.objects.filter(tickets__in=self.all())


class TicketManager(Manager.from_queryset(TicketQueryset)):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related('passenger', 'waypoint', 'order')
        )


class OrderManager(GuardedManager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(ticket_count=Count('tickets'))
        )
