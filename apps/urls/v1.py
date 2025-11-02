from django.urls import path, include


urlpatterns = [
    path('users/', include('apps.users.urls.v1')),
    path('products/', include('apps.products.urls.v1')),
    path('stories/', include('apps.stories.urls.v1')),
    path('cart/', include('apps.cart.urls.v1')),
    
    
]