from django.db.models import QuerySet, Manager


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
