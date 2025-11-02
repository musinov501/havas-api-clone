from django.dispatch import receiver
from django.db.models.signals import pre_save

from apps.products.models import Product


@receiver(pre_save, sender=Product)
def update_real_price_field(sender, instance, **kwargs):
    if instance.discount is None:
        instance.discount = 0
    if instance.discount < 0:
        raise ValueError("Discount cannot be negative")

    instance.real_price = instance.price - (instance.price * instance.discount / 100)