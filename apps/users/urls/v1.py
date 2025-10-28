from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

from apps.users.views.device import DeviceRegisterCreateAPIView, DeviceListApiView
from apps.users.views.user import UserRegisterAPIView, UserLoginAPIView

app_name = 'users'

urlpatterns = [
    path('devices/', DeviceRegisterCreateAPIView.as_view(), name='device-register'),
    path('devices/list/', DeviceListApiView.as_view(), name='device-list'),
    
    path('register/', UserRegisterAPIView.as_view(), name='user-register'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    
    
]




if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)