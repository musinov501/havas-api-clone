from django.db import models
from django.conf import settings
from apps.shared.models import BaseModel, Language
# Create your models here.


class NotificationType(models.TextChoices):
    PRODUCT = "PRODUCT", "Product"
    SYSTEM = "SYSTEM", "System"
    USER = "USER", "User"
    
    
class Notification(BaseModel):
    title = models.CharField(max_length = 255)
    message = models.TextField()
    type = models.CharField(max_length=20, choices=NotificationType.choices, default=NotificationType.SYSTEM)
    
    
    product = models.ForeignKey(
        'products.Product', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='notifications'
    )
    
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        null=True, blank=True, related_name='notifications'
        
    )
    
    is_read = models.BooleanField(default=False)
    language = models.CharField(max_length=3, choices=Language.choices, default=Language.UZ)
    
    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']
        
        def __str__(self):
            return f"{self.title} -> {self.recipient or "All users"}"