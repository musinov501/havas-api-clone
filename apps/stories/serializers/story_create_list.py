# from rest_framework import serializers
# from apps.stories.models import Story
# from apps.shared.mixins.translation_mixins import TranslatedFieldsWriteMixin, TranslatedFieldsReadMixin

# class StoryTranslationMixin:
#     translatable_fields = ['title', 'description', 'image']
#     media_fields = ['image']

# # -----------------------------
# # CREATE Serializer
# # -----------------------------
# class StoryCreateSerializer(
#     StoryTranslationMixin, TranslatedFieldsWriteMixin, serializers.ModelSerializer
# ):
#     image = serializers.ListField(
#         child=serializers.FileField(),
#         required=False,
#         allow_empty=True,
#         write_only=True  # Important: do not pass to Story model
#     )

#     class Meta:
#         model = Story
#         fields = [
#             'title', 'description', 'image',  # Keep in serializer for upload only
#             'story_type', 'start_date', 'end_date', 'is_active', 'product'
#         ]

#     def create(self, validated_data):
#         # Extract image so it's not passed to model.create()
#         media_data = {}
#         if 'image' in validated_data:
#             media_data['image'] = validated_data.pop('image')

#         # Extract translation fields
#         translation_fields = []
#         for field_name in getattr(self, "translatable_fields", []):
#             for lang_code, _ in self.languages:
#                 key = f"{field_name}_{lang_code.lower()}"
#                 if key in validated_data:
#                     translation_fields.append(key)
#                     validated_data.pop(key)

#         # Create Story instance without image/translation fields
#         story = Story.objects.create(**validated_data)

#         # Save media files
#         self._save_media_files(story, media_data)

#         return story


# # -----------------------------
# # LIST Serializer
# # -----------------------------
# class StoryListSerializer(StoryTranslationMixin, TranslatedFieldsReadMixin, serializers.ModelSerializer):
#     class Meta:
#         model = Story
#         fields = [
#             'id', 'title', 'description', 'image',
#             'story_type', 'start_date', 'end_date', 'created_at'
#         ]

#     def to_representation(self, instance):
#         """
#         Show one language if MOBILE device, all languages if WEB.
#         """
#         representation = super().to_representation(instance)
#         request = self.context.get('request')

#         # Default to Uzbek
#         lang = 'uz'
#         device_type = 'WEB'

#         if request:
#             device_type = getattr(request, 'device_type', 'WEB')
#             lang = getattr(request, 'lang', 'uz')

#         for field in self.translatable_fields:
#             if device_type == 'MOBILE':
#                 # Use only the requested language
#                 translated_value = getattr(instance, f"{field}_{lang}", None)
#                 representation[field] = translated_value or getattr(instance, field, None)
#                 # Remove any per-language fields
#                 for lc, _ in self.languages:
#                     representation.pop(f"{field}_{lc.lower()}", None)
#             else:
#                 # WEB → keep all language fields (fallback to base)
#                 for lc, _ in self.languages:
#                     per_attr = getattr(instance, f"{field}_{lc.lower()}", None)
#                     if per_attr in (None, ""):
#                         per_attr = getattr(instance, field, "")
#                     representation[f"{field}_{lc.lower()}"] = per_attr or ""
#                 # Remove base field to avoid duplication
#                 representation.pop(field, None)

#         return representation
