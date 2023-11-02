from django.db import models
from django.utils.functional import classproperty

from compat.django_guardian.models import GuardedModel

from event.models import Event

from .managers import TourManager, AgencyDependentManager


class AgencyDependentModel(GuardedModel):
    """An abstract base model class that represents a model that is dependent on an agency."""

    objects = AgencyDependentManager()

    class Meta:
        abstract = True

    @property
    def agency(self):
        """
        The agency related to the model.

        Usage:
            To use this property, define it in your subclass that extends `AgencyDependentModel`. The definition should
            provide a way to access the agency that the model is indirectly related to.

        Example:
            class MyModel(AgencyDependentModel):
                related_model = models.ForeignKey(RelatedModel, on_delete=models.CASCADE)

                @property
                def agency(self):
                    return self.related_model.agency

        In this example, `MyModel` is indirectly related to an agency through the `RelatedModel` that has a foreign
        key to the agency. The `agency` property is defined to return the agency of the related model.
        """
        raise NotImplemented('This property must be defined when the concrete model extending this class is indirectly'
                             ' related to the agency through another model that has a foreign key to the agency')

    @classproperty
    def agency_path(cls):
        """
        The path to the agency attribute in the model.

        This class property provides a way to access the path to the agency attribute in the model. By default, it is set
        to 'agency'. If the agency attribute is accessed through a different path in your concrete model, you should
        override this property to return the correct path.

        Usage:
            This property is used to access the path to the agency attribute in the model. If the agency attribute is
            accessed through a different path in your concrete model, you should override this property.

            Example:

            class MyModel(AgencyDependentModel):
                related_model = models.ForeignKey(RelatedModel, on_delete=models.CASCADE)

                @classproperty
                def agency_path(cls):
                    return 'related_model__agency'


            In this example, `MyModel` is indirectly related to an agency through the `RelatedModel` that has a foreign
            key to the agency. The `agency_path` property is overridden to return the correct path to the agency attribute.
        """
        return 'agency'

    def user_can_manage(self, user):
        """
        Checks if the given user has the 'manage_agency' permission for the agency related to the model.

        This method checks if the user has the 'manage_agency' permission for the agency that the model is indirectly
        related to. It uses the Django's built-in `has_perm` method to check the permission.
        """
        return user.has_perm('manage_agency', self.agency)


class Agency(GuardedModel):
    title = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = 'agencies'
        permissions = [('manage_agency', 'Can manage agency')]  # TODO: Define this in a global const

    def __str__(self):
        return self.title


class Tour(AgencyDependentModel):
    agency = models.ForeignKey(Agency, models.PROTECT)
    event = models.ForeignKey(Event, models.PROTECT)

    objects = TourManager()

    @property
    def heading(self):
        return f"Tour to '{self.event}' owned by '{self.agency}'."

    class Meta:
        ordering = ["agency"]

    def __str__(self):
        return self.heading
