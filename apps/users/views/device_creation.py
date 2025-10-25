from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from apps.users.models import Device
from apps.users.serializers import  DeviceSerializer



class DeviceListAPIView(generics.ListAPIView):
    serializer_class = DeviceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Device.objects.filter(user=self.request.user)