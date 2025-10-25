from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Device, User




class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone_number']
        
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            phone_number=validated_data.get('phone_number'),
            password=validated_data['password']
        )
        return user
        


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    device_id = serializers.CharField(write_only=True, required=False)
    device_name = serializers.CharField()
    device_type = serializers.CharField()
    operation_version = serializers.CharField()
    
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError('Invalid username or password')
        
        attrs['user'] = user
        return attrs
    
    
    def create(self, validated_data):
        user = validated_data['user']
        
        
        device_id = validated_data.get('device_id')
        if not device_id:
            import uuid
            device_id = str(uuid.uuid4())
        
        device, create = Device.objects.get_or_create(
            user=user,
            device_id=device_id,
            defaults={
                'device_name': validated_data['device_name'],
                'device_type': validated_data['device_type'],
                'operation_version': validated_data['operation_version'],
            }
        )
        
        device.generate_token()
        
        refresh = RefreshToken.for_user(user)
        
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'device_token': device.token,
            'device_name': device.device_name,
            'device_type': device.device_type
        }
        
        
    



class DeviceSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    token = serializers.CharField(read_only=True)
    
    
    class Meta:
        model = Device
        fields = [
            'id',
            'user',
            'device_id',
            'device_name',
            'device_type',
            'operation_version',
            'token',
            'registered_at',
        ]
        
        read_only_fields = ['id', 'token', 'registered_at']
        
        
    def create(self, validated_data):
        device = Device.objects.create(**validated_data)
        device.generate_token()
        return device