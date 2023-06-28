from django.db import models


class Agency(models.Model):
    title = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "agencies"
