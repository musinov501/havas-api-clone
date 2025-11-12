# from rest_framework.generics import ListCreateAPIView
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import status

# from apps.stories.models import Story
# from apps.stories.serializers.story_create_list import StoryCreateSerializer, StoryListSerializer
# from apps.stories.serializers.story_detail import StoryDetailSerializer
# from apps.shared.utils.custom_response import CustomResponse
# from apps.shared.utils.custom_pagination import CustomPageNumberPagination


# class StoryListCreateAPIView(ListCreateAPIView):
#     """
#     API endpoint to list or create Stories.
#     Mobile users get one language; Web users get all languages.
#     """
#     permission_classes = [IsAuthenticated]
#     pagination_class = CustomPageNumberPagination

#     def get_serializer_class(self):
#         if self.request.method == 'POST':
#             return StoryCreateSerializer
#         return StoryListSerializer

#     def get_queryset(self):
#         return Story.objects.filter(is_active=True)

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         page = self.paginate_queryset(queryset)

#         if page is not None:
#             serializer = self.get_serializer(page, many=True, context={'request': request})
#             return self.get_paginated_response(serializer.data)

#         serializer = self.get_serializer(queryset, many=True, context={'request': request})
#         return CustomResponse.success(
#             message_key="SUCCESS_MESSAGE",
#             data=serializer.data,
#             status_code=status.HTTP_200_OK
#         )

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         story = serializer.save()

#         response_serializer = StoryDetailSerializer(story, context={'request': request})
#         return CustomResponse.success(
#             message_key="SUCCESS_MESSAGE",
#             data=response_serializer.data,
#             status_code=status.HTTP_201_CREATED
#         )
