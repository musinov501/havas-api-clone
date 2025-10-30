from django.db import models
from apps.shared.models import BaseModel


class Measurement(models.TextChoices):
    GR = "GR", "Gram"
    PT = "PT", "Piece",
    L = "L" , "Litre"
    
    
    
class ProductCategory(models.TextChoices):
    BREAKFAST = "BREAKFAST", "Breakfast"
    LUNCH = "LUNCH", "Lunch"
    DINNER = "DINNER" , "Dinner"
    ALL = "ALL", "All Meals"
    



class Product(BaseModel):
    image = models.ImageField(upload_to='products/')
    title = models.CharField(max_length=255, db_index=True)
    
    description = models.TextField()
    
    price = models.DecimalField(max_digits=30, decimal_places=2)
    discount = models.PositiveSmallIntegerField(default=0)
    real_price = models.DecimalField(max_digits=30, decimal_places=2)
    
    category = models.CharField(
        choices=ProductCategory, 
        default=ProductCategory.ALL,
        db_index=True
        )
    measurement_type = models.CharField(
        choices=Measurement, 
        default=Measurement.GR
        )
    
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
         
    