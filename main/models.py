from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone

# Create your models here.




class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Access Denied. Must be a staff member to gain access.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Must be an admin to gain access.")

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    user_type_choices = (
        ('customer', 'Customer'),
        ('seller', 'Seller'),
        ('admin', 'Admin'),
    )
    user_type = models.CharField(max_length=20, choices=user_type_choices)
    dob = models.DateField()
    user_image = models.ImageField(upload_to='user_images', blank=True, null=True)
    phone_number = models.CharField(max_length=30)
    street_name = models.CharField(max_length=200)
    postcode = models.CharField(max_length=20)
    address = models.CharField(f"{street_name} {postcode}", max_length=200, blank=True)

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    


# Cart database

class Cart(models.Model):
    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'
        
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey('seller.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    date_created = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_paid = models.BooleanField(default=False)
    
    # Check if item is expired
    def is_expired(self):
        if self.is_active and self.is_paid == False:
            time_difference = timezone.now() - self.date_created
            if time_difference.days >= 30:
                return True  # Return True to indicate that the item is expired
        return False
    
    # Override the save method
    def save(self, *args, **kwargs):
        if self.is_expired():  # Check if the item is expired
            self.delete()  # Delete the item if not paid for after a 30 day period
            super().save(*args, **kwargs)  # Save the changes




# Order database

class Orders (models.Model):
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey('seller.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now_add=True, null=True)
    is_paid = models.BooleanField(default=False)
    is_processing = models.BooleanField(default=False)
    is_shipped = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    is_returned = models.BooleanField(default=False)
    is_refunded = models.BooleanField(default=False)
    
    
    # Check if order is paid and automatically marks it as processing
    
    def save (self, *args, **kwargs):
        if self.is_paid() == True:
            self.is_processing = True
        else:
            self.is_processing = False
        

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} {self.product.product_name} {self.quantity}"


    
# Order status database

class OrderStatus (models.Model):
    class Meta:
        verbose_name = 'Order Status'
        verbose_name_plural = 'Order Statuses'
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    status_choices = (
        ('paid', 'Paid'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('returned', 'Returned'),
        ('refunded', 'Refunded')
    )
    status = models.CharField(max_length=20, choices=status_choices)
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.order.user.first_name} {self.order.user.last_name} {self.order.product.product_name} {self.status}"
    


# Cart payment

class CartPayment (models.Model):
    class Meta:
        verbose_name = 'Cart Payment'
        verbose_name_plural = 'Cart Payments'
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    payment_type_choices = (
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('paypal', 'Paypal'),
    )
    payment_type = models.CharField(max_length=20, choices=payment_type_choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.date_paid} {self.cart}"
    



# Seller and delivery person payment preferences
class PaymentPreference (models.Model):
    class Meta:
        verbose_name = 'Payment Preference'
        verbose_name_plural = 'Payment Preferences'
    payment_type_choices = (
        ('bank_transfer', 'Bank Transfer'),
        ('paypal', 'Paypal'),
    )
    seller = models.ForeignKey('seller.Seller', on_delete=models.CASCADE, null=True)
    delivery = models.ForeignKey('delivery.DeliveryPerson', on_delete=models.CASCADE, null=True)
    payment_type = models.CharField(max_length=20, choices=payment_type_choices)
    bank_name = models.CharField(max_length=100, blank=True)
    account_number = models.CharField(max_length=20, blank=True)
    swift_code = models.CharField(max_length=20, blank=True)
    account_name = models.CharField(max_length=100, blank=True )
    paypal_email = models.EmailField(max_length=100, blank=True)
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.seller.user.first_name} {self.seller.user.last_name} {self.bank_name} {self.account_number} {self.swift_code} {self.account_name}"
        

            
            
    
    
    