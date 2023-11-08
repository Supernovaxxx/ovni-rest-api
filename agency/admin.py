import nested_admin

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from compat.django_guardian.admin import GuardedModelAdmin

from agency.models import Agency, Tour
from agency.sites import agency_admin_site
from trip.admin import TripAdminInline

from .utils import get_agency_for_user, get_agencies_for_user


@admin.register(Tour, site=admin.site)
@admin.register(Tour, site=agency_admin_site)
class TourAdmin(GuardedModelAdmin, nested_admin.NestedModelAdmin):
    list_display = ["heading", "event_details_link"]
    search_fields = ["event__title"]
    inlines = [TripAdminInline]

    @admin.display(description='Event Details')
    def event_details_link(self, obj):
        url = reverse("agency_admin:event_event_change", args=(obj.event.id,))
        return format_html("<a href='{}'>Event details</a>", url)

    def get_fields(self, request, obj=None):
        fields = ["event"]

        if get_agency_for_user(request.user):
            fields.insert(0, "agency")

        return fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "agency":
            kwargs["queryset"] = get_agencies_for_user(request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.agency = obj.agency or get_agency_for_user(request.user)
        super().save_model(request, obj, form, change)


@admin.register(Agency, site=admin.site)
@admin.register(Agency, site=agency_admin_site)
class AgencyAdmin(GuardedModelAdmin):
    pass


