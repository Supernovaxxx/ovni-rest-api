from django.contrib import admin

from guardian.admin import GuardedModelAdmin

from .models import Trip, Waypoint


@admin.register(Trip)
class TripAdmin(GuardedModelAdmin):
    list_display = ["tour", "slug", "departure", "capacity"]
    list_filter = ["departure", "capacity"]
    search_fields = ["tour__agency__title", "tour__event__title"]


@admin.register(Waypoint)
class WaypointAdmin(admin.ModelAdmin):
    list_display = ["title", "type", "trip", "place", "order"]
    list_filter = ["type", "order"]
    search_fields = [
        "trip__tour__agency__title",
        "trip__tour__event__title",
        "place__city",
        "place__state",
        "place__country",
    ]
