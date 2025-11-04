from django.db import models
from django.conf import settings
from apps.products.models import Product
# Create your models here.


class Recipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = 'recipes')
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    cook_time = models.PositiveIntegerField(help_text="Time in minutes")
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.title
    
    
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name = "ingredients")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField()
    unit = models.CharField(max_length=50)
    
    
    def __str__(self):
        return f"{self.quantity} {self.unit} of {self.product.title_en}"
    
    
    
    