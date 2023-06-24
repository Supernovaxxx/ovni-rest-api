from rest_framework import permissions


class IsOwnerIsStaff(permissions.BasePermission):
    """
    - Staff members have all permissions
    - Agency owners have object level edit and view permissions
    """
    def has_permission(self, request, view):

        if request.user.is_staff:
            return True
        
        # Remove create and delete actions from everyone but staff members.
        if request.method in ['POST', 'DELETE']: 
            return False
        
        return True
        
    def has_object_permission(self, request, view, obj):

        if request.user.is_staff:
            return True

        # Assign object level permission to the owner of the instance
        return obj.owner == request.user