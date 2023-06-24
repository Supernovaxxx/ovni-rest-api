from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Agency(models.Model):
    title = models.CharField(max_length=50)
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL) 

    class Meta:
        verbose_name_plural = 'agencies'


