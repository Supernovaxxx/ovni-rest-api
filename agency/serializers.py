from rest_framework import serializers

from guardian.shortcuts import get_objects_for_user

from .models import Agency, Tour


class ObjectPermissionFilteredForeignKey(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        return get_objects_for_user(user, "change_agency", Agency.objects.all(), accept_global_perms=False)


class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = '__all__'


class TourSerializer(serializers.ModelSerializer):
    agency = ObjectPermissionFilteredForeignKey()

    class Meta:
        model = Tour
        fields = '__all__'
