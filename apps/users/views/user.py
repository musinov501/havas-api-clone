from rest_framework import generics, status
from apps.users.serializers.user import UserRegisterSerializer, UserLoginSerializer
from apps.shared.utils.custom_response import CustomResponse
from apps.users.models.device import Device
from apps.users.serializers.device import DeviceListSerializer, DeviceRegisterSerializer


class UserRegisterAPIView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        device_token = serializer.validated_data.get("device_token")
        device = Device.objects.filter(device_token=device_token).first() if device_token else None

        data = {
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
            "device": DeviceListSerializer(device).data if device else None
        }

        return CustomResponse.success(
            message_key="USER_REGISTERED",
            data=data,
            status_code=status.HTTP_201_CREATED,
            request=request
        )

class UserLoginAPIView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            data={
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "devices": DeviceListSerializer(user.devices.all(), many=True).data
            }
        )


        