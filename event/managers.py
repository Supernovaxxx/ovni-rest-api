from django.db.models.functions import Now
from django.db.models import Manager, BooleanField, ExpressionWrapper, Q


class EventManager(Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                is_active=ExpressionWrapper(
                    Q(end_date__gte=Now()),
                    output_field=BooleanField(),
                ),
                is_upcoming=ExpressionWrapper(
                    Q(start_date__gt=Now()),
                    output_field=BooleanField(),
                ),
            )
        )

    def active(self):
        return self.filter(is_active=True)

    def upcoming(self):
        return self.filter(is_upcoming=True)
