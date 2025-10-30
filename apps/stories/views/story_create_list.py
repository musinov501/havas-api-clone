from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny
from apps.stories.serializers.story_create_list import StoryCreateSerializer, StoryListSerializer
from apps.shared.utils.custom_response import CustomResponse
from apps.stories.models import Story
from apps.shared.utils.custom_pagination import CustomPageNumberPagination
from rest_framework import status


class StoryListCreateAPIView(ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = StoryCreateSerializer
    pagination_class = CustomPageNumberPagination
    
    def get_queryset(self):
        return Story.objects.filter(is_active=True)
    
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        
        
        if page is not None:
            serializer = StoryListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = StoryListSerializer(queryset, many=True, context={'request': request})
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            data=serializer.data,
            status_code = status.HTTP_200_OK
        )
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            story = serializer.save()
            response_serializer = StoryListSerializer(story)
            return CustomResponse.success(
                message_key = "SUCCESS_MESSAGE",
                data=response_serializer.data,
                status_code = status.HTTP_201_CREATED
            )
        else:
            return CustomResponse.error(
                message_key="VALIDATION_ERROR",
                errors = serializer.errors
            )
            
            
