from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

from .models import AgencyDependentModel


class CanManageAgency(permissions.BasePermission):
    """Custom permission to be used along with 'AgencyDependentModels'"""

    def has_permission(self, request, view):
        if request.method == 'POST' and request.user.is_authenticated:
            return request.user.has_perm('agency.manage_agency')
        return True

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, AgencyDependentModel):

            if request.user.is_superuser:
                return True

            if request.method in SAFE_METHODS:
                if view.get_is_private:
                    return obj.user_can_manage(request.user)
                return True
            else:
                return obj.user_can_manage(request.user)

        else:
            raise ValueError("The object you're trying to access is not an instance of 'AgencyDependentModel'")
