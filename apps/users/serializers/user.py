
from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.users.models.device import Device
from apps.users.serializers.device import DeviceRegisterSerializer
from django.contrib.auth import authenticate

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    device_token = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ["username", "email", "password", "device_token"]

    def create(self, validated_data):
        device_token = validated_data.pop("device_token", None)
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

       
        if device_token:
            device, _ = Device.objects.get_or_create(device_token=device_token)
            device.user = user
            device.save(update_fields=["user"])

        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        data['user'] = user
        return data