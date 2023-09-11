from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

# Provides some extra views for object permissions management at admin panel.
from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import get_objects_for_user

from agency.models import Agency, Tour
from agency.sites import agency_admin_site
from trip.admin import TripAdminInline


@admin.register(Tour, site=agency_admin_site)
class TourAdmin(GuardedModelAdmin):
    list_display = ["tour", "event_details"]
    search_fields = ["event__title"]
    inlines = [TripAdminInline]

    def get_queryset(self, request):
        return get_objects_for_user(request.user, "agency.change_tour", accept_global_perms=False)

    def get_fields(self, request, obj=None):
        user_agency_count = Agency.objects.get_objects_for_user(request.user).count()
        if user_agency_count > 1:
            return ["event", "agency"]
        return ["event"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "agency":
            kwargs["queryset"] = Agency.objects.get_objects_for_user(request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.agency = obj.agency or Agency.objects.get_objects_for_user(request.user).first()
        super().save_model(request, obj, form, change)

    @admin.display()
    def tour(self, obj):
        return obj.__str__()

    @admin.display()
    def event_details(self, obj):
        url = reverse("agency_admin:event_event_change", args=(obj.event.id,))
        return format_html("<a href='{}'>Event details</a>", url)


@admin.register(Agency, site=agency_admin_site)
class AgencyAdmin(GuardedModelAdmin):
    def get_queryset(self, request):
        return Agency.objects.get_objects_for_user(request.user)
