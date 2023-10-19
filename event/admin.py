from datetime import datetime


from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from agency.sites import agency_admin_site
from event.models import Event


class IsUpcomingFilter(admin.SimpleListFilter):
    title = "upcoming"
    parameter_name = "is_upcoming"

    def lookups(self, request, model_admin):
        now = datetime.utcnow()
        qs = model_admin.get_queryset(request)

        if qs.filter(start_date__gt=now).exists():
            yield "Yes", "Yes"
        if qs.filter(start_date__lt=now).exists():
            yield "No", "No"

    def queryset(self, request, queryset):
        if value := self.value():
            now = datetime.utcnow()

            if value == "Yes":
                return queryset.filter(start_date__gt=now)
            else:
                return queryset.filter(start_date__lt=now)

        return queryset


@admin.register(Event, site=admin.site)
@admin.register(Event, site=agency_admin_site)
class EventAdmin(admin.ModelAdmin):
    list_display = ["title", "start_date", "end_date", "create_tour_link"]
    list_filter = ["start_date", "end_date", IsUpcomingFilter]
    fields = [("title", "subtitle"), ("start_date", "end_date")]
    search_fields = ["title"]

    @staticmethod
    def create_tour_link(obj):
        url = reverse("agency_admin:agency_tour_add")
        url += f"?event={obj.id}"
        return format_html("<a href='{}'>Create Tour</a>", url)
