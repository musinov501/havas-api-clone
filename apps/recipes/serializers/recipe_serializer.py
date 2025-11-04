from rest_framework import serializers
from apps.products.models import Product
from apps.recipes.models import Recipe, RecipeIngredient
from apps.products.serializers.product_list_create import ProductListSerializer


class RecipeIngredientSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        write_only=True
    )
    
    class Meta:
        model = RecipeIngredient
        fields = ["id", "product", "product_id", "quantity", "unit"]
        
        
class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(many=True)
    
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'image', 'cook_time', 'ingredients']
        
        
    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients', [])
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients_data:
            product = ingredient.pop('product_id')
            RecipeIngredient.objects.create(recipe=recipe, product=product, **ingredient)
        return recipe



    
    