from drf_writable_nested import (
    NestedCreateMixin,
    NestedUpdateMixin,
)
from rest_framework.serializers import *


class ModelSerializer(ModelSerializer):

    @classmethod
    def with_meta(cls, **kwargs):
        kwargs.setdefault('model', cls.Meta.model)

        return type(cls.__name__, (cls,), {
            'Meta': type('Meta', (), kwargs)
        })


class WriteableNestedModelSerializer(NestedCreateMixin, NestedUpdateMixin, ModelSerializer):
    pass
