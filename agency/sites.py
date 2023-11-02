from django.contrib import admin

from .utils import get_agency_for_user


class AgencyAdminSite(admin.AdminSite):
    site_title = "Agency site admin"
    site_header = "Agency administration"

    def has_permission(self, request):
        return get_agency_for_user(request.user).exists()


agency_admin_site = AgencyAdminSite(name="agency_admin")
