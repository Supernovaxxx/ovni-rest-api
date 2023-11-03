from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

from .models import AgencyDependentModel
from .utils import get_agencies_for_user


class CanManageAgency(permissions.BasePermission):
    """Custom permission to be used along with 'AgencyDependentModels'"""

    def has_permission(self, request, view):
        user = request.user

        if request.method == 'POST':
            if user.is_authenticated:
                return user.has_perm('agency.manage_agency')
            return False

        elif view.get_is_private:
            return get_agencies_for_user(user).exists()

        return True

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, AgencyDependentModel):

            if request.user.is_superuser:
                return True

            if request.method in SAFE_METHODS:
                return True

            return obj.user_can_manage(request.user)

        else:
            raise ValueError("The object you're trying to access is not an instance of 'AgencyDependentModel'")
