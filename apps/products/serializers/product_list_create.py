from rest_framework import serializers

from apps.products.models import Product

class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['real_price', 'created_at', 'updated_at', 'uuid']
        
        
class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'