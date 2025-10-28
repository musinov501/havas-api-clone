from rest_framework.permissions import BasePermission
from apps.shared.exceptions.custom_exceptions import CustomException
from apps.users.models.device import Device

class IsMobileUser(BasePermission):
    def has_permission(self, request, view):
        token = request.headers.get('Token')  

        if not token:
            raise CustomException(message_key="TOKEN_IS_NOT_PROVIDED")

        try:
            device = Device.objects.get(device_token=token)
        except Device.DoesNotExist:
            raise CustomException(message_key="INVALID_TOKEN")

  
        request.device = device

        return True 
