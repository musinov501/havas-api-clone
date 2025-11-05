from rest_framework import serializers
from apps.notifications.models import Notification
from apps.products.models import Product


class ProductMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'real_price']


class NotificationSerializer(serializers.ModelSerializer):
    product = ProductMiniSerializer(read_only=True) 

    class Meta:
        model = Notification
        fields = [
            'id',
            'title',
            'message',
            'is_read',
            'created_at',
            'product',
        ]
