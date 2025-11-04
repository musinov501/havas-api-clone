from django.db import models
from django.conf import settings
from apps.products.models import Product



class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default="My Meal List")
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"Cart of {self.user.username} - {self.name}"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True, null=True)
    
    
    def __str__(self):
        return f"{self.product.title} (x{self.quantity})"
    
    
    @property
    def estimated_price(self):
        return self.quantity * self.product.price
    
    
