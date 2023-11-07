from rest_framework.exceptions import ValidationError

from .models import AgencyRelatedModel


class UserCanManage:
    requires_context = True

    def __call__(self, obj, serializer):
        if isinstance(obj, AgencyRelatedModel) and not obj.user_can_manage(serializer.context['request'].user):
            raise ValidationError(f"You don't have permission to manage the {obj} with id: `{obj.id}`.")
