from rest_framework import serializers
from apps.cart.models import Cart, CartItem
from apps.products.models import Product
from apps.products.serializers.product_list_create import ProductListSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        write_only=True
    )
    
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'notes', 'estimated_price', 'product_id']
        
    
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero!")
        return value
    
        
    def create(self, validated_data):
        product = validated_data.pop('product_id')
        return CartItem.objects.create(product=product, **validated_data)
        
        

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'name', 'created_at', 'items']
        


