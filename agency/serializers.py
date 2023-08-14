from rest_framework import serializers

from .models import Agency, Tour


class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = "__all__"


class TourSerializer(serializers.ModelSerializer):
    agency = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Tour
        fields = "__all__"
