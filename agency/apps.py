from django.contrib.admin import apps


class AgencyConfig(apps.AdminConfig):
    default_site = "agency.sites.AgencyAdminSite"
    default_auto_field = "django.db.models.BigAutoField"
    name = "agency"

    def ready(self):
        super().ready()
        import agency.signals.handlers
