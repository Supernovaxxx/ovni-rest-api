from rest_framework import viewsets, permissions

from .models import Agency
from .serializers import AgencySerializer
from .permissions import IsReadOnly


class AgencyViewSet(viewsets.ModelViewSet):
    queryset = Agency.objects.all()
    serializer_class = AgencySerializer
    permission_classes = [permissions.DjangoObjectPermissions|IsReadOnly]
