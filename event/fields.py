from django.db.models.functions import Now
from django.db.models import Q, BooleanField

from generic.fields import AnnotationField


IsUpcomingAnnotationField = AnnotationField.create_subclass_from_expression(
    function=Q(end_date__gte=Now()),
    output_field=BooleanField(),
)
