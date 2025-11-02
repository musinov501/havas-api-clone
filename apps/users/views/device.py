from typing import Any

from rest_framework import generics, permissions, status
from rest_framework.pagination import PageNumberPagination
from apps.shared.permissions.mobile import IsMobileUser
from apps.shared.utils.custom_response import CustomResponse
from apps.users.models.device import Device
from apps.users.serializers.device import DeviceListSerializer, DeviceRegisterSerializer


class DeviceRegisterCreateAPIView(generics.CreateAPIView):
   
    serializer_class = DeviceRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.device = None

    def perform_create(self, serializer):
        device = serializer.save()
        self.device = device

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            response.data['device_token'] = str(self.device.device_token)
            return CustomResponse.success(
                message_key="SUCCESS_MESSAGE",
                data=response.data,
                status_code=status.HTTP_201_CREATED
            )
        except Exception as e:
            import traceback
            print("🔥 DEVICE CREATE ERROR:", traceback.format_exc())
            return CustomResponse.error(
                message_key="UNKNOWN_ERROR",
                message=str(e)
            )






class DeviceListApiView(generics.ListAPIView):
    serializer_class = DeviceListSerializer
    permission_classes = [IsMobileUser]  
    pagination_class = PageNumberPagination
    
    def get_queryset(self):
        return Device.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
      
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                "id": "SUCCESS_MESSAGE",
                "message": "Operation completed successfully",
                "data": serializer.data
            })

        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            data=serializer.data,
            request=request,
            status_code=200
        )

