from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.cart.models import Cart, CartItem
from apps.products.models import Product
from django.contrib.auth import get_user_model


User = get_user_model()


class CartApiTestCase(APITestCase):
    
    
    def setUp(self):
        self.user = User.objects.create_user(
            username = 'testuser',
            password = 'testpass123'
        )
        
        self.client.force_authenticate(user=self.user)
        
        self.cart = Cart.objects.create(user=self.user, name='Test Cart')
        self.product = Product.objects.create(
            title = "Test Product",
            description = "A product for testing",
            price = 10.50
            
        )
        
        self.cart_url = reverse('cart:cart-list-create')
        self.cart_item_url = reverse('cart:cart-item-create')
        

    
    def test_add_item_to_cart(self):
        payload = {
            "cart": self.cart.id,
            "product_id": self.product.id,
            "quantity": 2,
            "notes": "Testing notes"
        }
        
        response = self.client.post(self.cart_item_url, payload, format='json')
        print("RESPONSE:", response.data) 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CartItem.objects.count(), 1)
        self.assertEqual(CartItem.objects.first().product, self.product)
        
        
    def test_get_cart_items(self):
        CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity = 1,
            notes = "Simple test"
        )
        
        response = self.client.get(self.cart_url)
        
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('items', response.data['results'][0])
        
        
    def test_delete_cart_item(self):
        
        item = CartItem.objects.create(
            cart = self.cart,
            product=self.product,
            quantity = 1
        )
        
        url = reverse('cart:cart-item-update-delete', args=[item.id])
        response = self.client.delete(url)
        
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CartItem.objects.filter(id=item.id).exists())
        
        
    
    def test_add_item_invalid_product(self):
      
        payload = {
            "product_id": 9999,
            "quantity": 1
        }

        response = self.client.post(self.cart_item_url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('product_id', response.data)

    def test_add_item_with_zero_quantity(self):
   
        payload = {"product_id": self.product.id, "quantity": 0}
        response = self.client.post(self.cart_item_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_item_with_negative_quantity(self):
  
        payload = {"product_id": self.product.id, "quantity": -3}
        response = self.client.post(self.cart_item_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthorized_user_cannot_access_cart(self):

        self.client.force_authenticate(user=None)
        response = self.client.get(self.cart_url)
        self.assertEqual(response.status_code,  status.HTTP_403_FORBIDDEN)

    def test_automatic_cart_creation(self):

        new_user = User.objects.create_user(username='newuser', password='1234')
        self.client.force_authenticate(user=new_user)
        payload = {"product_id": self.product.id, "quantity": 1}
        response = self.client.post(self.cart_item_url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Cart.objects.filter(user=new_user).exists())

    def test_list_multiple_carts(self):
      
        Cart.objects.create(user=self.user, name='Cart 2')
        Cart.objects.create(user=self.user, name='Cart 3')

        response = self.client.get(self.cart_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 2)

    def test_delete_empty_cart(self):
       
        cart = Cart.objects.create(user=self.user, name='Empty Cart')
        cart.delete()
        self.assertFalse(Cart.objects.filter(id=cart.id).exists())