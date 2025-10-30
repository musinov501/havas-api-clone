from rest_framework import serializers
from apps.stories.models import Story, Survey, SurveyOption


class StoryListSerializer(serializers.ModelSerializer):
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
            'created_at'
        ]
        

class StoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = [
            'title',
            'description',
            'image',
            'story_type',
            'start_date',
            'end_date',
            'is_active',
            'product'
        ]
        
    def validate(self, data):
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError("End date must be after start date")
        return data