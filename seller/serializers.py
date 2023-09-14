from .models import Seller, Category, Review, Product, SellerDashboard
from rest_framework import serializers

# Seller serializer model object

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = '__all__'
        


# Category serializer model object 

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        


# Review serializer model object

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        
        
# Product serializer model object

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        
        

# Seller dashboard serializer model object

class SellerDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerDashboard
        fields = '__all__'
        


