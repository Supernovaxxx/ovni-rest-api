from django.contrib import admin

from .models import Place


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ["place_id", "formatted_address", "google_maps_link"]
    search_fields = ["city", "state", "country"]
