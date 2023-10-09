from dal import autocomplete

from .models import Place


class PlaceAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Place.objects.none()

        qs = Place.objects.all()

        if self.q:
            qs = qs.filter(formatted_address__icontains=self.q)

        return qs
