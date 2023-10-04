import nested_admin


from trip.models import Waypoint, Trip
from .forms import WaypointForm


class WaypointAdminInline(nested_admin.NestedStackedInline):
    model = Waypoint
    extra = 0
    form = WaypointForm


class TripAdminInline(nested_admin.NestedStackedInline):
    model = Trip
    extra = 0
    inlines = [WaypointAdminInline]
