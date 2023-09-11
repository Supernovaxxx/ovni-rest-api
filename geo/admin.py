from django.contrib import admin
from django.utils.html import format_html

from .models import Place


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ["place_id", "formatted_address", "google_maps_link"]
    search_fields = ["city", "state", "country"]

    @admin.display()
    def google_maps_link(self, obj):
        return format_html(
            '<a href="{}">GoogleMaps</a>',
            obj.google_maps_url,
        )