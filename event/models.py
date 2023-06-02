from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()