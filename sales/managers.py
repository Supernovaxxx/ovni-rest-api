from django.db.models import Manager, Count

from agency.managers import AgencyDependentManager, AgencyDependentQuerySet


class TicketQueryset(AgencyDependentQuerySet):
    def passengers(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        return User.objects.filter(tickets__in=self.all())


class TicketManager(Manager.from_queryset(AgencyDependentQuerySet)):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related('passenger', 'waypoint', 'order', 'waypoint__trip__tour__agency')
        )


class OrderManager(AgencyDependentManager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(ticket_count=Count('tickets'))
        )
