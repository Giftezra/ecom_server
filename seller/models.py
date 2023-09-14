# Module imports

from django.db import models
from geopy.geocoders import Nominatim
from django.core.exceptions import ValidationError
from main.models import Orders, PaymentPreference


# Seller database
class Seller (models.Model):
    class Meta:
        verbose_name = 'Seller'
        verbose_name_plural = 'Sellers'
    user = models.ForeignKey('main.CustomUser', on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=100)
    shop_street = models.CharField(max_length=200, blank=False)
    shop_postcode = models.CharField(max_length=20, blank=False)
    latitude = models.DecimalField(max_digits=10, max_length=10, decimal_places=5, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, max_length=10, decimal_places=5, blank=True, null=True)
    
    
    # Convert the seller address to longitude and latitude
    # This will enable the algorithm to display products based on the distance from the buyer
    def save(self, *args, **kwargs):
            if self.street and self.postcode:
                shop_address = f"{self.street} {self.postcode}"
                geolocator = Nominatim(user_agent="anyi")
                location = geolocator.geocode(shop_address)

                if location:
                    self.latitude = location.latitude
                    self.longitude = location.longitude
                else:
                    raise ValidationError("Address not found") # Throw an error if address not found

            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} {self.shop_name} {self.latitude} {self.longitude}"
    
    
    
# Product category database

class Category (models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    category_type_choices = (
        ('staples', 'Staples'),
        ('protiens', 'Protiens'),
        ('vegetables', 'Vegetables'),
        ('spices and condiments', 'Spices and Condiments'),
        ('snacks', 'Snacks'),
        ('hair care', 'Hair Care'),
        ('skin care', 'Skin Care'),
        ('herbal and wellness', 'Herbal and Wellness'),
    )
    
    categor_type = models.CharField(max_length=50, choices=category_type_choices)
    
    def __str__(self):
        return f"{self.category_type}"

    
    
# Products database

class Product (models.Model):
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='product_images', blank=True)
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product_nameproduct_description} {self.product_price} {self.product_quantity}"




# Review and rating database

class Review (models.Model):
    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
    user = models.ForeignKey('main.CustomUser', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.CharField(max_length=200)
    rating = models.IntegerField()
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} {self.product.product_name} {self.rating}"
    



# Seller dashboard database

class SellerDashboard (models.Model):
    class Meta:
        verbose_name = 'Seller Dashboard'
        verbose_name_plural = 'Seller Dashboards'
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    best_selling_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    best_selling_days = models.DateField(max_length=100)
    order_management = models.ForeignKey(Orders, on_delete=models.CASCADE)
    total_orders = models.IntegerField()
    total_sales = models.DecimalField(max_digits=10, decimal_places=2)
    total_products = models.IntegerField()
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.seller.user.first_name} {self.seller.user.last_name} {self.total_orders} {self.total_sales} {self.total_products}"
    
    
    
    
# Product on sale database
# This will be used to display products on sale

class ProductOnSale (models.Model):
    class Meta:
        verbose_name = 'Product On Sale'
        verbose_name_plural = 'Products On Sales'
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_start_date = models.DateField()
    sale_end_date = models.DateField()
    is_on_sale = models.BooleanField(default=False)
    date_created = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product.name} {self.sale_price} {self.sale_start_date} {self.sale_end_date} {self.is_on_sale}"
    
    
