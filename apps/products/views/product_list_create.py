from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny
from apps.products.serializers.product_list_create import ProductCreateSerializer, ProductListSerializer
from apps.shared.utils.custom_response import CustomResponse
from apps.products.models import Product
from apps.shared.utils.custom_pagination import CustomPageNumberPagination
from rest_framework import status

class ProductListCreateAPIView(ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductCreateSerializer
    pagination_class = CustomPageNumberPagination
    
  
    
    def get_queryset(self):
        return Product.objects.filter(is_active=True)
    
    
    def list(self, request, *args, **kwargs):
        pass
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            response_serializer = ProductListSerializer(product)
            return CustomResponse.success(
                message_key="SUCCESS_MESSAGE",
                data=response_serializer.data,
                status_code=status.HTTP_201_CREATED,
            
            )
        else:
            return CustomResponse.error(
                message_key="VALIDATION_ERROR",
                errors=serializer.errors
            )
    