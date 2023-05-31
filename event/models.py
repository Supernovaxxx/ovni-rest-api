from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    start_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False)