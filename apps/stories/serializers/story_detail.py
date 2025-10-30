from rest_framework import serializers
from apps.stories.models import Story, Survey, SurveyOption


class SurveyOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyOption
        fields = ['id', 'option_text', 'order']


class SurveySerializer(serializers.ModelSerializer):
    options = SurveyOptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Survey
        fields = ['id', 'question', 'options']

class StoryDetailSerializer(serializers.ModelSerializer):
    survey = SurveySerializer(read_only=True)
    
    class Meta:
        model = Story
        fields = [
            'id',
            'title',
            'description',
            'image',
            'story_type',
            'start_date',
            'end_date',
            'product',
            'survey',
            'created_at'
        ]