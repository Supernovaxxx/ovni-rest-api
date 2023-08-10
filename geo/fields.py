from django.db.models import CharField, Value
from django.db.models.functions import Concat

from generic.fields import AnnotationField


class CoordinateAnnotationField(AnnotationField):
    def __init__(self, **kwargs):
        super().__init__(
            function=Concat('latitude', Value(','), 'longitude'),
            output_field=CharField(),
            **kwargs
        )


GoogleMapsURLAnnotationField = AnnotationField.create_subclass_from_expression(
    function=Concat(
        Value('https://www.google.com/maps/search/'),
        Value('?api=1'),
        Value('&query='), 'country',
        Value('&query_place_id='), 'place_id',
    ),
    output_field=CharField(),
)
