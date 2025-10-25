import secrets
from django.contrib.auth.models import AbstractUser
from apps.shared.models import BaseModel 
from django.db import models

# Create your models here.


class User(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    is_customer = models.BooleanField(default=True)
    is_manager = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.username
    
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        
    
    

    
class Device(BaseModel):
    
    DEVICE_CHOICES = [
        ('ios', 'iOS'),
        ('android', 'Android'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')
    device_id = models.CharField(max_length=255, unique=True)
    device_name = models.CharField(max_length=100)
    device_type = models.CharField(max_length=50)
    operation_version = models.CharField(max_length=50)
    token = models.CharField(max_length=255, blank=True, null=True, unique=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.device_name} ({self.device_type})"
    
    
    def generate_token(self):
        self.token = secrets.token_hex(32)
        self.save(update_fields=['token'])  
    
    
    class Meta:
        verbose_name = 'Device'
        verbose_name_plural = 'Devices'
        

        
    
    