from django.db import models

from . import managers


class GuardedModel(models.Model):

    objects = managers.GuardedManager()

    class Meta:
        abstract = True
