# apps/notifications/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.products.models import Product
from .models import Notification

@receiver(post_save, sender=Product)
def send_product_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            title="New product added!",
            message=f"{instance.title} is now available.",
            type="PRODUCT",
            product=instance,
        )
