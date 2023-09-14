from rest_framework import serializers
from .models import CustomUser, Cart, Orders, OrderStatus, CartPayment, PaymentPreference

# Use rest framework to serialize the custom user model

class CustomUserSerializer (serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        
        
# Use rest framework to serialize the cart model
 
class CartSerializer (serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
        
        
        
# Use rest framework to serialize the cart payment model

class OrdersSerializer (serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'
        
    

# Use rest framework to serialize the order status model
class OrderStatusSerializer (serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = '__all__'
        

# Use rest framework to serialize the cart payment model
class CartPaymentSerializer (serializers.ModelSerializer):
    class Meta:
        model = CartPayment
        fields = '__all__'
        
        
        
# Use rest framework to serialize the payment preference model
class PaymentPreferenceSerializer (serializers.ModelSerializer):
    class Meta:
        model = PaymentPreference
        fields = '__all__'
        
