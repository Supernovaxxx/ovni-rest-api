import functools

from django.db.models import Field, ExpressionWrapper
from django.utils.functional import cached_property

"""
Heavily inspired by django-models-extensions's VirtualFunctionField
See https://github.com/lampofearth/django-models-extensions/blob/master/django_models_extensions/models/fields/__init__.py
"""


class ReadOnlyField(Field):
    empty_strings_allowed = False

    def __init__(self, **kwargs):
        super().__init__(**dict(kwargs, editable=False, null=True, blank=True, default=None))

    def db_type(self, connection):
        return None

    def formfield(self, **kwargs):
        return None


class AnnotationField(ReadOnlyField):
    description = "Virtual function field. Returns function result."

    def __init__(self, function, output_field=None, **kwargs):
        super().__init__(**kwargs)
        self.function = function
        self.output_field = output_field

    @cached_property
    def expression(self):
        expression = ExpressionWrapper(self.function, self.output_field)
        expression.target = self
        return expression

    @cached_property
    def cached_col(self):
        attname = self.get_attname()

        queryset = self.model.objects.all()
        queryset._fields = {'id'}

        queryset = queryset.annotate(**{attname: self.expression}).values_list(attname)
        return queryset.query.annotations[attname]

    def get_col(self, alias, output_field=None):
        return self.cached_col

    @classmethod
    def create_subclass_from_expression(cls, function, output_field=None):
        return type(
            str(function) + cls.__name__,
            (cls,),
            {
                '__module__': cls.__module__,
                '__init__': functools.partialmethod(cls.__init__, function=function, output_field=output_field),
            },
        )
