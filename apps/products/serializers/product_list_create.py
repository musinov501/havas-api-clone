from rest_framework import serializers
from apps.products.models import Product
from apps.shared.mixins.translation_mixins import (
    TranslatedFieldsWriteMixin,
    TranslatedFieldsReadMixin
)


class ProductTranslationMixin:
    translatable_fields = ['title', 'description', 'images']
    media_fields = ['images']


# -----------------------------
# CREATE / UPDATE Serializer
# -----------------------------
class ProductCreateSerializer(
    ProductTranslationMixin, TranslatedFieldsWriteMixin, serializers.ModelSerializer
):
    class Meta:
        model = Product
        fields = [
            'title', 'description', 'price',
            'measurement_type', 'is_active', 'category', 'discount'
        ]


# -----------------------------
# LIST / GET Serializer
# -----------------------------
class ProductListSerializer(
    ProductTranslationMixin, TranslatedFieldsReadMixin, serializers.ModelSerializer
):
    class Meta:
        model = Product
        fields = [
            'id', 'uuid', 'price', 'real_price',
            'measurement_type', 'created_at', 'is_active',
            'category', 'discount', 'title', 'description'
        ]
   


# -----------------------------
# DETAIL Serializer
# -----------------------------
class ProductDetailSerializer(
    ProductTranslationMixin, TranslatedFieldsReadMixin, serializers.ModelSerializer
):
    class Meta:
        model = Product
        fields = [
            'id', 'uuid', 'title', 'description',
            'price', 'real_price', 'measurement_type',
            'created_at', 'is_active', 'category', 'discount'
        ]
   
