from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

from apps.users.views.register_user import (
    RegisterAPIView,
    LoginAPIView,
    )
from apps.users.views.device_creation import DeviceListAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='user-register'),
    path('login/', LoginAPIView.as_view(), name='user-login'),
    
    path('devices/', DeviceListAPIView.as_view(), name='device-list'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)