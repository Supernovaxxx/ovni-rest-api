import nested_admin

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from compat.django_guardian.admin import GuardedModelAdmin

from agency.models import Agency, Tour
from agency.sites import agency_admin_site
from trip.admin import TripAdminInline


@admin.register(Tour, site=agency_admin_site)
class TourAdmin(GuardedModelAdmin, nested_admin.NestedModelAdmin):
    list_display = ["heading", "event_details_link"]
    search_fields = ["event__title"]
    inlines = [TripAdminInline]

    @admin.display(description='Event Details')
    def event_details_link(self, obj):
        url = reverse("agency_admin:event_event_change", args=(obj.event.id,))
        return format_html("<a href='{}'>Event details</a>", url)

    @staticmethod
    def get_agency_queryset_for_user(request):
        return Agency.objects.for_user(request.user)

    def get_fields(self, request, obj=None):
        fields = ["event"]

        if self.get_agency_queryset_for_user(request).first():
            fields.insert(0, "agency")

        return fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "agency":
            kwargs["queryset"] = self.get_agency_queryset_for_user(request)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.agency = obj.agency or self.get_agency_queryset_for_user(request).first()
        super().save_model(request, obj, form, change)


@admin.register(Agency, site=agency_admin_site)
class AgencyAdmin(GuardedModelAdmin):
    pass
