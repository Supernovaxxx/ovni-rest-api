from django.db.models import QuerySet, Manager


class DistinctQuerySet(QuerySet):

    @property
    def kind(self):
        return self.model.__kind__

    def create(self, **kwargs):
        if self.kind:
            kwargs.update({'kind': self.kind})
        return super(DistinctQuerySet, self).create(**kwargs)


class DistinctManager(Manager.from_queryset(DistinctQuerySet)):

    @property
    def kind(self):
        return self.model.__kind__

    def get_queryset(self):
        queryset = super(DistinctManager, self).get_queryset()
        if self.kind:
            queryset = queryset.filter(kind=self.kind)
        return queryset
