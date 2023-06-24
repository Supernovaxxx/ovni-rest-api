from rest_framework import viewsets
from .models import Agency
from .serializers import ForStaffAgencySerializer, ForOwnerAgencySerializer
from .permissions import IsOwnerIsStaff


class AgencyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerIsStaff,]
    
    def get_queryset(self):
        if self.request.user.is_anonymous:
            return []
        
        if self.request.user.is_superuser:
            return Agency.objects.all()
        
        user = self.request.user
        
        return Agency.objects.filter(owner=user)
    
    def get_serializer_class(self):
        if self.request.user.is_staff:
            return ForStaffAgencySerializer
        return ForOwnerAgencySerializer
