from django.utils.module_loading import autodiscover_modules

from agency import sites


def autodiscover():
    autodiscover_modules("admin", register_to=sites.agency_admin_site)
