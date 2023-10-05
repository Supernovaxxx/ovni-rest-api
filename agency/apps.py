from django.contrib.admin import apps
from django.utils.module_loading import autodiscover_modules

from agency import sites


class AgencyConfig(apps.SimpleAdminConfig):
    default_site = "agency.sites.AgencyAdminSite"
    default_auto_field = "django.db.models.BigAutoField"
    name = "agency"

    def ready(self):
        super().ready()
        autodiscover_modules("admin", register_to=sites.agency_admin_site)
        import agency.signals.handlers
