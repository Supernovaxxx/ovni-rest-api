from django.contrib import admin

from guardian.admin import GuardedModelAdmin

from .models import Agency


# Provides some extra views for object permissions management at admin panel.
class AgencyAdmin(GuardedModelAdmin):
    pass


admin.site.register(Agency, AgencyAdmin)