from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.models.device import AppVersion, DeviceType, Device



class DeviceRegisterApiTestCase(APITestCase):
    def test_device_register_success(self):
        response = self.client.post(path=self.url, data=self.base_payload)
        
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertIn('device_token', response.json().get('data'))
        self.assertTrue(Device.objects.filter(device_id=self.base_payload['device_id']).exists())
        
        
    
    def test_device_register_missing_required_field(self):
        required_fields = ['device_model', 'device_type', 'device_id', 'app_version']
        
        for field in required_fields:
            payload = self.base_payload.copy()
            del payload[field]
            
            response = self.client.post(path=self.url, data=payload)
            
            self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
            self.assertIn(field, response.json())
            
            