from django.contrib import admin

from guardian.admin import GuardedModelAdmin

from .models import Trip


class TripAdmin(GuardedModelAdmin):
    pass


admin.site.register(Trip, TripAdmin)
