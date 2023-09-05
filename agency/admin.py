from django.contrib import admin

# Provides some extra views for object permissions management at admin panel.
from guardian.admin import GuardedModelAdmin

from .models import Agency, Tour


@admin.register(Tour)
class AgencyAdmin(GuardedModelAdmin):
    list_display = ["title"]
    search_fields = ["title"]


@admin.register(Agency)
class TourAdmin(GuardedModelAdmin):
    list_display = ["id", "agency", "event"]
    search_fields = ["agency__title", "event__title"]
