
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
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid username or password")

        if not user.check_password(data['password']):
            raise serializers.ValidationError("Invalid username or password")

        data['user'] = user
        return data