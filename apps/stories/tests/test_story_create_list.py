# from django.urls import reverse_lazy
# from rest_framework.test import APITestCase
# from django.core.files.uploadedfile import SimpleUploadedFile
# from apps.stories.models import Story, Survey, SurveyOption, SurveyResponse
# from apps.users.models.user import User
# from apps.users.models.device import Device
# from apps.products.models import Product
# from django.utils import timezone


# class TestStoryCreateList(APITestCase):
#     def setUp(self):
#         self.url = reverse_lazy('stories:story-list-create')

#         # create a small in-memory image for tests
#         image_content = (
#             b'\x47\x49\x46\x38\x39\x61\x02\x00'
#             b'\x01\x00\x80\x00\x00\x00\x00\x00'
#             b'\xFF\xFF\xFF\x21\xF9\x04\x01\x00'
#             b'\x00\x00\x00\x2C\x00\x00\x00\x00'
#             b'\x02\x00\x01\x00\x00\x02\x02\x4C'
#             b'\x01\x00\x3B'
#         )
#         image_file = SimpleUploadedFile('story.gif', image_content, content_type='image/gif')

#         self.payload = {
#             'image': image_file,
#             'title': 'Milk Story',
#             'description': 'This is a story about milk products.',
#             'story_type': 'promo',
#             'start_date': timezone.now(),
#             'end_date': timezone.now() + timezone.timedelta(days=7),
#             'is_active': True
#         }

#     def test_create_story_success(self):
#         response = self.client.post(path=self.url, data=self.payload, format='multipart')
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(response.data['data']['title'], self.payload['title'])

#     def test_list_stories(self):
#         Story.objects.create(
#             image=self.payload['image'],
#             title=self.payload['title'],
#             description=self.payload['description'],
#             story_type=self.payload['story_type'],
#             start_date=self.payload['start_date'],
#             end_date=self.payload['end_date'],
#             is_active=self.payload['is_active']
#         )
#         response = self.client.get(path=self.url)
#         self.assertEqual(response.status_code, 200)
#         # Custom pagination response uses 'count' on the paginated response; adapt if your project uses a different format
#         self.assertEqual(response.data['count'], 1)

#     def test_create_story_missing_fields(self):
#         invalid_payload = self.payload.copy()
#         invalid_payload.pop('title')
#         response = self.client.post(path=self.url, data=invalid_payload, format='multipart')
#         self.assertEqual(response.status_code, 400)
#         self.assertIn('title', response.data['errors'] if 'errors' in response.data else response.data)

#     def test_invalid_story_type(self):
#         invalid_payload = self.payload.copy()
#         invalid_payload['story_type'] = 'invalid_type'
#         response = self.client.post(path=self.url, data=invalid_payload, format='multipart')
#         self.assertEqual(response.status_code, 400)
#         self.assertIn('story_type', response.data['errors'] if 'errors' in response.data else response.data)

#     def test_invalid_date_range(self):
#         invalid_payload = self.payload.copy()
#         invalid_payload['start_date'] = timezone.now()
#         invalid_payload['end_date'] = timezone.now() - timezone.timedelta(days=1)
#         response = self.client.post(path=self.url, data=invalid_payload, format='multipart')
#         self.assertEqual(response.status_code, 400)
#         self.assertIn('end_date', str(response.data))

#     def test_create_story_with_product(self):
#         product = Product.objects.create(
#             title_en="Milk",
#             title_uz="Sut",
#             description_en="Natural milk",
#             description_uz="Tabiiy sut",
#             price=100.00,
#             category="ALL",
#             measurement_type="L",
#             is_active=True
#         )

#         payload = self.payload.copy()
#         payload['product'] = product.id
#         response = self.client.post(path=self.url, data=payload, format='multipart')
#         self.assertEqual(response.status_code, 201)
#         self.assertIn('data', response.data)

#     def test_create_story_with_survey(self):
#         # create a story first (Survey.story is required)
#         story = Story.objects.create(
#             image=self.payload['image'],
#             title=self.payload['title'],
#             description=self.payload['description'],
#             story_type='survey',
#             start_date=self.payload['start_date'],
#             end_date=self.payload['end_date'],
#             is_active=True
#         )

#         # create survey attached to story using correct field names
#         survey = Survey.objects.create(story=story, question="Which one do you like?")
#         SurveyOption.objects.create(survey=survey, option_text="Option A")
#         SurveyOption.objects.create(survey=survey, option_text="Option B")

#         payload = self.payload.copy()
#         payload['story'] = story.id  # or pass survey id if your create endpoint expects it

#         response = self.client.post(path=self.url, data=payload, format='multipart')

#         self.assertEqual(response.status_code, 201)
#         self.assertIn('data', response.data)