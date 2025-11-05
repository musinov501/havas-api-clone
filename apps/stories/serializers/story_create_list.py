from rest_framework import serializers
from apps.stories.models import Story
from apps.shared.mixins.translation_mixins import TranslatedFieldsWriteMixin, TranslatedFieldsReadMixin

# -----------------------------
# TRANSLATION MIXIN
# -----------------------------
class StoryTranslationMixin:
    # Fields that need translation
    translatable_fields = ['title', 'description', 'image']  
    media_fields = ['image'] 


# -----------------------------
# CREATE / UPDATE Serializer
# -----------------------------
class StoryCreateSerializer(
    StoryTranslationMixin, TranslatedFieldsWriteMixin, serializers.ModelSerializer
):
    class Meta:
        model = Story
        fields = [
            'title', 'description', 'image',
            'story_type', 'start_date', 'end_date', 'is_active', 'product'
        ]
        set_translations = serializers.CharField(
        max_length=2,
        required=False,
        help_text="Language code, 2 characters"
    )
    

    def create(self, validated_data):
        """
        Handle creation of Story with translations.
        """
        # Pop translation fields from validated_data
        translations = {}
        for field in self.translatable_fields:
            for lang in ['uz', 'en']:
                key = f"{field}_{lang}"
                if key in validated_data:
                    translations[key] = validated_data.pop(key)

        
        story = Story.objects.create(**validated_data)

      
        self.set_translations(story, translations)

        return story

    def validate(self, data):
        """
        Ensure end_date is after start_date.
        """
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError("End date must be after start date")
        return data


# -----------------------------
# LIST Serializer
# -----------------------------
class StoryListSerializer(
    StoryTranslationMixin, TranslatedFieldsReadMixin, serializers.ModelSerializer
):
    class Meta:
        model = Story
        fields = [
            'id', 'title', 'description', 'image',
            'story_type', 'start_date', 'end_date', 'created_at'
        ]


# -----------------------------
# DETAIL Serializer
# -----------------------------
class StoryDetailSerializer(
    StoryTranslationMixin, TranslatedFieldsReadMixin, serializers.ModelSerializer
):
    class Meta:
        model = Story
        fields = [
            'id', 'title', 'description', 'image',
            'story_type', 'start_date', 'end_date', 'product', 'created_at'
        ]
