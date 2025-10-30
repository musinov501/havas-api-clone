from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from apps.products.serializers.product_list_create import ProductListSerializer
from apps.shared.utils.custom_response import CustomResponse
from apps.products.models import Product
from rest_framework import status

class ProductRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
      permission_classes = [AllowAny]
      serializer_class = ProductListSerializer
      lookup_field = 'pk'
      
      def get_queryset(self):
         return Product.objects.filter(is_active=True)
      
      def retrieve(self, request, *args, **kwargs):
         instance = self.get_object()
         serializer = self.get_serializer(instance)
         return CustomResponse.success(
               message_key="SUCCESS_MESSAGE",
               data=serializer.data,
               status_code=status.HTTP_200_OK,
               
         )
