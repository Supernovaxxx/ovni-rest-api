from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"

    def save(self, **kwargs):
        try:
            return super().save(**kwargs)
        except Exception as e:
            raise serializers.ValidationError(str(e))
