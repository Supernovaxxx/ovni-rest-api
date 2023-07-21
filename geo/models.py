from django.db import models
from django.utils.translation import gettext_lazy as _

from django_countries.fields import CountryField


class Place(models.Model):
    class States(models.TextChoices):
        AC = "AC"
        AL = "AL"
        AP = "AP"
        AM = "AM"
        BA = "BA"
        CE = "CE"
        DF = "DF"
        ES = "ES"
        GO = "GO"
        MA = "MA"
        MT = "MT"
        MS = "MS"
        MG = "MG"
        PA = "PA"
        PB = "PB"
        PR = "PR"
        PE = "PE"
        PI = "PI"
        RJ = "RJ"
        RN = "RN"
        RS = "RS"
        RO = "RO"
        RR = "RR"
        SC = "SC"
        SP = "SP"
        SE = "SE"
        TO = "TO"

    title = models.TextField(max_length=50)
    detail = models.TextField(max_length=255)
    formatted_address = models.TextField(max_length=50)
    city = models.TextField(max_length=50)
    state = models.CharField(max_length=2, choices=States.choices)
    country = CountryField()
    latitude = models.DecimalField(decimal_places=2, max_digits=50)
    longitude = models.DecimalField(decimal_places=2, max_digits=50)
