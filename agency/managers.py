from django.db.models import Sum, Count, Manager

from compat.django_guardian.managers import GuardedQuerySet

from .utils import get_agencies_for_user, get_agency_for_user


class AgencyDependentQuerySet(GuardedQuerySet):
    @property
    def agency_path(self):
        """Returns the agency path attribute of the model."""
        return self.model.agency_path

    def for_user(self, user, actions=('manage',), lookup_name='in'):
        """
        Returns a queryset with all the objects related to the user's agency.

        Args:
            user: The user for whom to retrieve the objects.
            actions: The actions for which to retrieve the objects. Defaults to ('manage',).
            lookup_name: The lookup name to use for the agency path. Defaults to 'in'.

        Returns:
            A queryset containing the objects related to the user's agency.
        """
        lookup = self._concatenate_lookup(lookup_name, user, actions)
        return self.filter(**lookup)

    def _concatenate_lookup(self, lookup_name, user, actions):
        """
        Concatenates the lookup name with the agency path to create the lookup parameter.

        Args:
            lookup_name: The lookup name to concatenate with the agency path.
            user: The user for whom to retrieve the agencies.
            actions: The actions for which to retrieve the agencies.

        Returns:
            A dictionary containing the lookup parameter.
        """
        if lookup_name:
            return {self.agency_path + '__' + lookup_name: get_agencies_for_user(user, actions)}
        return {self.agency_path: get_agency_for_user(user, actions)}


class AgencyDependentManager(Manager.from_queryset(AgencyDependentQuerySet)):
    pass


class TourManager(AgencyDependentManager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(revenue=Sum('trips__route__tickets__order__value'))
            .annotate(passenger_count=Count('trips__route__tickets__passenger'))
        )
