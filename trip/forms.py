from dal import autocomplete

from django import forms

from .models import Waypoint


class WaypointForm(forms.ModelForm):
    class Meta:
        model = Waypoint
        exclude = ["order"]
        widgets = {
            'place': autocomplete.ModelSelect2(url='place-autocomplete')
        }
