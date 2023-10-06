from django.contrib import admin


class AgencyAdminSite(admin.AdminSite):
    site_title = "Agency site admin"
    site_header = "Agency administration"

    def has_permission(self, request):
        from agency.models import Agency
        return Agency.objects.for_user(request.user).exists()


agency_admin_site = AgencyAdminSite(name="agency_admin")
