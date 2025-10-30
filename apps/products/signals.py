from django.dispatch import receiver
from django.db.models.signals import pre_save

from apps.products.models import Product


@receiver(pre_save, sender=Product)
def update_real_price_field(sender, instance, **kwargs):
    if instance.discount > 0:
        instance.real_price = instance.price - (instance.price * instance.discount / 100)
    elif instance.discount > 100:
        raise ValueError("Discount cannot be greater than 100%")
    else:
        raise ValueError("Discount cannot be negative")
    