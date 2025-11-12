from django.db import models
from apps.shared.models import BaseModel
from apps.products.models import Product
from apps.users.models.device import Device
from apps.users.models.user import User



class Story(BaseModel):
    STORY_TYPES = (
        ('promo', 'Promotional'),
        ('survey', 'Survey'),
    )
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    story_type = models.CharField(max_length=20, choices=STORY_TYPES)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        db_table = 'stories'
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title
    
    @property
    def media_files(self):
        """Return related media files."""
        from django.contrib.contenttypes.models import ContentType
        from apps.shared.models import Media
        
        content_type = ContentType.objects.get_for_model(self)
        return Media.objects.filter(content_type=content_type, object_id=self.pk)
    
class Survey(BaseModel):
    story = models.OneToOneField(Story, on_delete=models.CASCADE, related_name='survey')
    question = models.TextField()
    
    class Meta:
        db_table = 'surveys'
    
    
    def __str__(self):
        return f"Survey for: {self.story.title}"
    
    
class SurveyOption(BaseModel):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=255)
    order = models.IntegerField(default=0)
    
    
    class Meta:
        db_table = 'survey_options'
        ordering = ['order']
        
    def __str__(self):
        return self.option_text
    
class SurveyResponse(BaseModel):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='responses')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(SurveyOption, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, null=True)
    
    
    class Meta:
        db_table = 'survey_responses'
        unique_together = ['survey', 'user'] 
        
    
    def __str__(self):
        return f"{self.user} answered {self.survey}"
    
