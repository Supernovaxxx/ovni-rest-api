from datetime import datetime, UTC


from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from agency.sites import agency_admin_site
from event.models import Event


class IsUpcomingFilter(admin.SimpleListFilter):
    title = 'upcoming'
    parameter_name = 'is_upcoming'

    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Yes'),
            ('No', 'No'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return queryset.filter(start_date__gt=datetime.now(UTC))
        elif value == 'No':
            return queryset.exclude(start_date__gt=datetime.now(UTC))
        return queryset


@admin.register(Event, site=agency_admin_site)
class EventAdmin(admin.ModelAdmin):
    list_display = ["title", "start_date", "end_date", "is_upcoming", "create_tour_link"]
    list_filter = ["start_date", "end_date", IsUpcomingFilter]
    fields = [("title", "subtitle"), ("start_date", "end_date")]
    search_fields = ["title"]

    def is_upcoming(self, obj):
        return obj.start_date > datetime.now(UTC)

    @admin.display()
    def create_tour_link(self, obj):
        url = reverse("agency_admin:agency_tour_add")
        url += f"?event={obj.id}"
        return format_html("<a href='{}'>Create Tour</a>", url)
