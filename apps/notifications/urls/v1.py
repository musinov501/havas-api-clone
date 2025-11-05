from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from apps.notifications.views.create_list import NotificationViewSet
app_name = 'notifications'

router = DefaultRouter()
router.register(r'', NotificationViewSet, basename='notifications')

urlpatterns = router.urls



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)