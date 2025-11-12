# from rest_framework import serializers
# from apps.stories.models import Story, Survey, SurveyOption
# from apps.shared.mixins.translation_mixins import TranslatedFieldsWriteMixin, TranslatedFieldsReadMixin
# from apps.stories.serializers.story_create_list import StoryTranslationMixin



# class StoryDetailSerializer(
#     StoryTranslationMixin, TranslatedFieldsReadMixin, serializers.ModelSerializer
# ):
#     class Meta:
#         model = Story
#         fields = [
#             'id', 'title', 'description', 'image',
#             'story_type', 'start_date', 'end_date', 'product', 'created_at'
#         ]
    
#     def to_representation(self, instance):
#         """
#         Customize the output to include translated fields.
#         """
#         representation = super().to_representation(instance)
        
#         # Get the language from request (default to 'uz')
#         request = self.context.get('request')
#         lang = 'uz'  # default
#         if request:
#             lang = request.headers.get('Accept-Language', 'uz')[:2]
        
#         # Override fields with translated versions if they exist
#         for field in self.translatable_fields:
#             translated_field = f"{field}_{lang}"
#             if hasattr(instance, translated_field):
#                 translated_value = getattr(instance, translated_field)
#                 if translated_value:  # Only override if translation exists
#                     representation[field] = translated_value
        
#         return representation