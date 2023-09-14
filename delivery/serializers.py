# Import libraries and models

from rest_framework import serializers
from .models import DeliveryPerson, DeliveryMethod, DeliveryStatus, DeliveredItems

# Delivery person serializer

class DeliveryPersonSerializer (serializers.ModelSerializer):
    class Meta:
        model = DeliveryPerson
        fields = '__all__'
        
        

# Delivery method serializer

class DeliveryMethodSerializer (serializers.ModelSerializer):
    class Meta:
        model = DeliveryMethod
        fields = '__all__'
        
        

# Delivery status serializer

class DeliveryStatusSerializer (serializers.ModelSerializer):
    class Meta:
        model = DeliveryStatus
        fields = '__all__'
        



# Delivered items serializer

class DeliveredItemsSerializer (serializers.ModelSerializer):
    class Meta:
        model = DeliveredItems
        fields = '__all__'
        