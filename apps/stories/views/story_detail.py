from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from apps.stories.serializers.story_detail import StoryDetailSerializer
from apps.shared.utils.custom_response import CustomResponse
from apps.stories.models import Story
from rest_framework import status


class StoryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    serializer_class = StoryDetailSerializer
    lookup_field = 'pk'
    
    
    def get_queryset(self):
        return Story.objects.filter(is_active=True)
    
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context = {'request': request})
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )