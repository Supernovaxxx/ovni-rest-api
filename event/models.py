from django.db import models


class Event(models.Model):
    title = models.TextField()
    subtitle = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        ordering = ["-start_date"]
