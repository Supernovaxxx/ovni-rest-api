from django.contrib.auth.models import GroupManager


class GroupTypeManager(GroupManager):

    @property
    def kind(self):
        return self.model.__kind__

    def get_queryset(self):
        return super().get_queryset().prefetch_related('permissions')

    def get_by_natural_key(self, name):
        return self.get(kind=self.kind, name=name)


class ModelGroupQuerySet:

    @property
    def kind(self):
        return self.model.__kind__

    def create(self, **kwargs):
        related_fieldname = self.kind.lower()

        related_object = kwargs.get(related_fieldname, None)
        if not related_object:
            raise ValueError(
                f'`{related_fieldname}` is required to create {self.kind}Group '
                f'through ' + ModelGroupQuerySet.__name__
            )

        related_object.group = super(ModelGroupQuerySet, self).create(**{
            related_fieldname: related_object,
            'name': related_object.__str__(),
        })
        related_object.save()
        return related_object.group
