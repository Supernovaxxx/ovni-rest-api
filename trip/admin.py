from django.contrib import admin

from guardian.admin import GuardedModelAdmin

from .models import Trip, Waypoint


class TripAdmin(GuardedModelAdmin):
    pass


admin.site.register(Trip, TripAdmin)
admin.site.register(Waypoint)
