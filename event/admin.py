from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["title", "start_date", "end_date"]
    list_filter = ["start_date", "end_date"]
    fields = [("title", "subtitle"), ("start_date", "end_date")]
    search_fields = ["title"]
