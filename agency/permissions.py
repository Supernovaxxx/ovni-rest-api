from rest_framework import permissions

from .models import AgencyRelatedModel


class CanManageAgency(permissions.DjangoObjectPermissions):
    perms_map = {
        'GET': [],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s', 'agency.manage_agency'],
        'PUT': ['%(app_label)s.change_%(model_name)s', 'agency.manage_agency'],
        'PATCH': ['%(app_label)s.change_%(model_name)s', 'agency.manage_agency'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s', 'agency.manage_agency'],
    }

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, AgencyRelatedModel):
            return super().has_object_permission(request, view, obj.agency)
        raise ValueError('Object must be an `AgencyRelatedModel` instance.')
