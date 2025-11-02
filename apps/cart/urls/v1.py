from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from apps.cart.views.cart_create_list import CartListCreateAPIView, CartItemCreateAPIView, CartItemUpdateDeleteAPIView


app_name = 'cart'

urlpatterns = [
    path('', CartListCreateAPIView.as_view(), name='cart-list-create'),
    path('items/', CartItemCreateAPIView.as_view(), name='cart-item-create'),
    path('items/<int:pk>/', CartItemUpdateDeleteAPIView.as_view(), name='cart-item-update-delete')
]





if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)