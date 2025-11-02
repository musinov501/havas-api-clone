from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from apps.products.models import Product
import os

User = get_user_model()


class TestProductCreate(APITestCase):
    def setUp(self):
        self.url = reverse_lazy('products:product-list-create')

       
        self.user = User.objects.create_user(
            phone_number="+998901234567",
            password="testpassword123",
            is_staff=True,
            is_superuser=True
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    
        image_path = r"C:\Users\Noutbukcom\programming\7_oy\lesson8\media\products\img.jpg"
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Test image not found: {image_path}")

        with open(image_path, "rb") as img:
            self.image_file = SimpleUploadedFile(
                "milk.jpg", img.read(), content_type="image/jpeg"
            )

        self.payload = {
            "title_uz": "Sut",
            "title_en": "Milk",
            "description_uz": "Tabiiy sut",
            "description_en": "Natural milk",
            "price": "100.00",
            "discount": 10,
            "category": "ALL",
            "measurement_type": "L",
            "is_active": True,
            "images_uz": self.image_file,
        }

    def test_create_product_success(self):
        response = self.client.post(self.url, data=self.payload, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("data", response.data)
        self.assertEqual(response.data["data"]["title"], "Sut")

    def test_check_discount_calculation(self):
        response = self.client.post(self.url, data=self.payload, format="multipart")
        product = Product.objects.last()
        expected_real_price = float(self.payload["price"]) * (1 - self.payload["discount"] / 100)
        self.assertAlmostEqual(float(product.real_price), expected_real_price, places=2)

    def test_create_product_missing_fields(self):
        invalid_data = self.payload.copy()
        invalid_data.pop("price")
        response = self.client.post(self.url, data=invalid_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("price", str(response.data))

    def test_duplication_fields(self):
        self.client.post(self.url, data=self.payload, format="multipart")
        response = self.client.post(self.url, data=self.payload, format="multipart")
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])

    def test_invalid_payload(self):
        invalid_data = self.payload.copy()
        invalid_data["price"] = "not_a_number"
        response = self.client.post(self.url, data=invalid_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("price", str(response.data))

    def test_category_type(self):
        invalid_data = self.payload.copy()
        invalid_data["category"] = "INVALID"
        response = self.client.post(self.url, data=invalid_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("category", str(response.data))

    def test_measurement_type(self):
        invalid_data = self.payload.copy()
        invalid_data["measurement_type"] = "INVALID"
        response = self.client.post(self.url, data=invalid_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("measurement_type", str(response.data))


    def test_get_product_list(self):
        self.client.post(self.url, data=self.payload, format="multipart")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertTrue(len(response.data['results']) > 0)
        
    
    def test_get_product_detail(self):
        create_response = self.client.post(self.url, data=self.payload, format="multipart")
        product_id = create_response.data["data"]["id"]
        detail_url = reverse_lazy("products:product-detail", kwargs={"pk": product_id})
        
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['title_uz'], "Sut")
        
        
        
    def test_get_product_detail(self):
        create_response = self.client.post(self.url, data=self.payload, format="multipart")
        product_id = create_response.data["data"]["id"]
        detail_url = reverse_lazy("products:product-detail", kwargs={"pk": product_id})
        
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['title_en'], "Milk")
        
        
        