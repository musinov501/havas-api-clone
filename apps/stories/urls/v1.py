# from django.conf import settings
# from django.urls import path
# from django.conf.urls.static import static
# from apps.stories.views.story_create_list import StoryListCreateAPIView
# from apps.stories.views.story_detail import StoryRetrieveUpdateDestroyAPIView

# app_name = 'stories'

# urlpatterns = [
#     path('', StoryListCreateAPIView.as_view(), name='story-list-create'),
#     path('<int:pk>/', StoryRetrieveUpdateDestroyAPIView.as_view(), name='story-detail')
# ]





# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)