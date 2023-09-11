from django.contrib import admin

from guardian.admin import GuardedModelAdmin

from trip.models import Waypoint, Trip
from agency import sites


class WaypointAdminInline(admin.StackedInline):
    model = Waypoint
    extra = 0


class TripAdminInline(admin.StackedInline):
    model = Trip
    extra = 0
