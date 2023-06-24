from rest_framework import serializers
from .models import Agency


class ForOwnerAgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = '__all__'
        read_only_fields = ['owner',]


class ForStaffAgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = '__all__'