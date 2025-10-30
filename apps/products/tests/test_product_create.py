

from django.urls import reverse_lazy
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
import os


class TestProductCreate(APITestCase):
    def setUp(self):
        self.url = reverse_lazy('products:product-list-create')

        image_path = r"C:\Users\Noutbukcom\programming\7_oy\lesson8\media\products\img.jpg"

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Test image not found: {image_path}")

        with open(image_path, 'rb') as img:
            image_file = SimpleUploadedFile('milk.jpg', img.read(), content_type='image/jpeg')

        self.payload = {
            "image": image_file,
            "title": "Organic Milk",
            "description": "Fresh organic milk from local farms.",
            "price": "100.00",
            "discount": 10,
            "category": "ALL",
            "measurement_type": "L",
            "is_active": True
        }

    def test_create_product_success(self):
        response = self.client.post(path=self.url, data=self.payload, format='multipart')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['data']['title'], self.payload['title'])

    
    def test_check_discount_calculation(self):
        pass
    
    def test_create_product_missing_fields(self):
        pass
    
    def test_duplication_fields(self):
        pass
    
    def test_invalid_payload(self):
        pass
    
    def test_category_type(self):
        pass
    
    def test_measurement_type(self):
        pass
    
    