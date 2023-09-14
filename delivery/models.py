from django.db import models

from geopy.geocoders import Nominatim


# Create your models here.

class DeliveryPerson (models.Model):
    class Meta:
        verbose_name = 'Delivery Person'
        verbose_name_plural = 'Delivery People'
    user = models.ForeignKey('main.CustomUser', on_delete=models.CASCADE)
    document_type_choices = (
        ('passport', 'Passport'),
        ('drivers license', 'Drivers License'),
        ('national id', 'National ID'),
        ('biometric Residence Permit', 'Biometric Residence Permit')
    )
    payment_preference = models.OneToOneField('main.PaymentPreference', on_delete=models.CASCADE)
    document_type = models.CharField(max_length=50, choices=document_type_choices)
    document = models.ImageField(upload_to='delivery_person_documents', blank=True, null=True)
    current_latitude = models.DecimalField(max_digits=10, max_length=10, decimal_places=5, blank=True, null=True)
    current_longitude = models.DecimalField(max_digits=10, max_length=10, decimal_places=5, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} {self.current_latitude} {self.current_longitude}"



# Deivery method database

class DeliveryMethod (models.Model):
    class Meta:
        verbose_name = 'Delivery Method'
        verbose_name_plural = 'Delivery Methods'
    delivery_method_choices = (
        ('bike', 'Bike'),
        ('motorcycle', 'Motorcycle'),
        ('car', 'Car'),
    )
    delivery_method = models.CharField(max_length=50, choices=delivery_method_choices)
    delivery_personel = models.ForeignKey(DeliveryPerson, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.delivery_method
    


# Delivery status database

class DeliveryStatus (models.Model):
    class Meta:
        verbose_name = 'Delivery Status'
        verbose_name_plural = 'Delivery Statuses'
    delivery = models.ForeignKey(DeliveryMethod, on_delete=models.CASCADE)
    deliver_personel = models.ForeignKey(DeliveryPerson, on_delete=models.CASCADE)
    order = models.ForeignKey('main.Orders', on_delete=models.CASCADE)
    is_delivered = models.BooleanField(default=False)
    is_enroute = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
                
            
    
    def __str__(self):
        return self
    
    
    
# Delivered Items database

class DeliveredItems (models.Model):
    class Meta:
        verbose_name = 'Delivered Item'
        verbose_name_plural = 'Delivered Items'
    delivery_person = models.ForeignKey(DeliveryPerson, on_delete=models.CASCADE)
    order = models.ForeignKey('main.Orders', on_delete=models.CASCADE)
    num_items_delivered = models.IntegerField(default=0)
    is_delivered = models.BooleanField(default=False)
    delivery_date = models.DateField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.delivery_person} {self.order} {self.num_items_delivered} {self.is_delivered} {self.delivery_date}"