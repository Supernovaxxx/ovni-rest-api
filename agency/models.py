from django.contrib.auth.models import User
from django.db import models


class Agency(models.Model):
    title = models.CharField(max_length=50)
    manager = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "agencies"
