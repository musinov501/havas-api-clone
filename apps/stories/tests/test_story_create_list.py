from django.urls import reverse_lazy
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.stories.models import Story, Survey, SurveyOption, SurveyResponse
from apps.users.models.user import User
from apps.users.models.device import Device
from apps.products.models import Product
import os
from django.utils import timezone



class TestStoryCreateList(APITestCase):
    def setUp(self):
        self.url = reverse_lazy('stories:story-list-create')
        image_path = r"C:\Users\Noutbukcom\programming\7_oy\lesson8\media\stories\story_img.jpg"
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Test image not found: {image_path}")
        
        with open(image_path, 'rb') as img:
            image_file = SimpleUploadedFile('story.jpg', img.read(), content_type='image/jpeg')
            
        self.payload = {
            'image': image_file,
            'title': 'Milk Story',
            'description': 'This is a story about milk products.',
            'story_type': 'promo',
            'start_date': timezone.now(),
            'end_date': timezone.now() + timezone.timedelta(days=7),
            'is_active': True
        }
        
        
    def test_create_story_success(self):
        response = self.client.post(path=self.url, data=self.payload, format='multipart')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['data']['title'], self.payload['title'])
        
        
    def test_list_stories(self):
        Story.objects.create(
            image = self.payload['image'],
            title = self.payload['title'],
            description = self.payload['description'],
            story_type = self.payload['story_type'],
            start_date = self.payload['start_date'],
            end_date = self.payload['end_date'],
            is_active = self.payload['is_active']
                )
        response = self.client.get(path=self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        
            
        
    def test_create_story_missing_fields(self):
        invalid_payload = self.payload.copy()
        invalid_payload.pop('title')
        response = self.client.post(path=self.url, data=invalid_payload, format='multipart')
        self.assertEqual(response.status_code, 400)
        self.assertIn('title', response.data['errors'])
    
    def test_invalid_story_type(self):
        invalid_payload = self.payload.copy()
        invalid_payload['story_type'] = 'invalid_type'
        response = self.client.post(path=self.url, data=invalid_payload, format='multipart')
        self.assertEqual(response.status_code, 400)
        self.assertIn('story_type', response.data['errors'])
    
    def test_invalid_date_range(self):
        invalid_payload = self.payload.copy()
        invalid_payload['start_date'] = timezone.now()
        invalid_payload['end_date'] = timezone.now() - timezone.timedelta(days=1)
        response = self.client.post(path=self.url, data=invalid_payload, format='multipart')
        self.assertEqual(response.status_code, 400)
        self.assertIn('end_date', str(response.data))
    
    def test_create_story_with_product(self):
        product = Product.objects.create(
            title_en = "Milk",
            title_uz = "Sut",
            description_en = "Natural milk",
            description_uz = "Tabiiy sut",
            price = 100.00,
            category = "ALL",
            measurement_type = "L",
            is_active = True
        )
        
        payload = self.payload.copy()
        payload['product'] = product.id
        response = self.client.post(path=self.url, data=payload, format='multipart')
        self.assertEqual(response.status_code, 201)
        self.assertIn('data', response.data)
        
        
    
    def test_create_story_with_survey(self):
        survey = Survey.objects.create(title="Which one do you like?")
        SurveyOption.objects.create(survey=survey, text="Option A")
        SurveyOption.objects.create(survey=survey, text="Option B")

        payload = self.payload.copy()
        payload['survey'] = survey.id
        response = self.client.post(path=self.url, data=payload, format='multipart')

        self.assertEqual(response.status_code, 201)
        self.assertIn('data', response.data)
    
    
    

        