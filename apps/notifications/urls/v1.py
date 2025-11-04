from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from apps.products.views.product_list_create import ProductListCreateAPIView
from apps.products.views.product_detail import ProductRetrieveUpdateDestroyAPIView

app_name = 'notifications'

urlpatterns = [
    
]





if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)