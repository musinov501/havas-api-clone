from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from apps.products.models import Product
from apps.products.serializers.product_list_create import (
    ProductListSerializer,
    ProductDetailSerializer,
    ProductCreateSerializer
)
from apps.shared.permissions.mobile import IsMobileOrWebUser
from apps.shared.utils.custom_response import CustomResponse


class ProductRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsMobileOrWebUser]
    lookup_field = 'pk'

    def get_queryset(self):
        return Product.objects.filter(is_active=True)

    def get_serializer_class(self):
   
        if self.request.method in ['PUT', 'PATCH']:
            return ProductCreateSerializer
        elif self.request.method == 'GET':
            return ProductDetailSerializer
        return ProductListSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                message_key="UPDATED_SUCCESSFULLY",
                data=serializer.data,
                status_code=status.HTTP_200_OK
            )
        return CustomResponse.error(
            message_key="VALIDATION_ERROR",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return CustomResponse.success(
            message_key="DELETED_SUCCESSFULLY",
            data=None,
            status_code=status.HTTP_204_NO_CONTENT
        )
