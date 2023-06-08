from django.utils import timezone
from django.db.models import Manager, BooleanField, ExpressionWrapper, Q


class EventManager(Manager):
    def active(self):
        qs = self.annotate(
            is_active=ExpressionWrapper(
                Q(end_date__gte=timezone.now()),
                output_field=BooleanField(),
            )
        )
        return qs.filter(is_active=True)
