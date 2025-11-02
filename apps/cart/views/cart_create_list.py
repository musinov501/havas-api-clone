from rest_framework import generics, permissions
from apps.cart.models import Cart, CartItem
from apps.cart.serializers.cart_create import CartSerializer, CartItemSerializer


class CartListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
        

class CartItemCreateAPIView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
    def perform_create(self, serializer):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)
        
        
class CartItemUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    
    
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)
    

        
    