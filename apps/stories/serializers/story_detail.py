from rest_framework import serializers
from apps.stories.models import Story, Survey, SurveyOption
from apps.shared.mixins.translation_mixins import TranslatedFieldsWriteMixin, TranslatedFieldsReadMixin
from apps.stories.serializers.story_create_list import StoryTranslationMixin


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
            'story_type', 'start_date', 'end_date', 'created_at',
            'product'
        ]
