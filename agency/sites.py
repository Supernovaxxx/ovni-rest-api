from django.contrib import admin


class AgencyAdminSite(admin.AdminSite):
    site_title = "Agency site admin"
    site_header = "Agency administration"

    def has_permission(self, request):
        return super().has_permission(request) or request.user.groups.filter(name__contains="Managers").exists()  # TODO Find a trustworthy way to catch user's groups.


agency_admin_site = AgencyAdminSite(name="agency_admin")
