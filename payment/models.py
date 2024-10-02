from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import datetime

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    shipping_full_name = models.CharField(max_length=255)
    shipping_email = models.CharField(max_length=255)
    shipping_address1 = models.CharField(max_length=255)
    shipping_address2 = models.CharField(max_length=255, null=True, blank=True)
    shipping_city = models.CharField(max_length=255)
    shipping_state = models.CharField(max_length=255, blank= True, null=True)
    shipping_zipcode = models.CharField(max_length=255, blank=True, null=True)
    shipping_country = models.CharField(max_length=255)
    
    class Meta:
        verbose_name_plural = 'Shipping Address'
        
    def __str__(self):
        return f"Shipping address: {str(self.id)}"

# Create order model
class Order(models.Model):
    # forign key
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    
    full_name = models.CharField(max_length=260)
    email = models.EmailField(max_length=260)
    shipping_address = models.TextField(max_length=15000)
    amount_paid = models.DecimalField(max_digits=15, decimal_places=2)
    date_ordered = models.DateField(auto_now_add=True)
    shipped = models.BooleanField(default=False)
    shipped_date = models.DateTimeField(blank=True, null=True)
    # show the order id in admin section
    def __str__(self):
        return f'Order: {str(self.id)}'


# Auto add a shipping date
@receiver(pre_save, sender=Order)
def set_shipped_date(sender, instance, **kwargs):
    if instance.pk:
        now = datetime.datetime.now()
        obj = sender._default_manager.get(pk=instance.pk)
        if instance.shipped and not obj.shipped:
            instance.shipped_date = now
            
        

# Create order items model
class OrderItem(models.Model):
    #forign keys
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    
    # show the order id in admin section
    def __str__(self):
        return f'Order Item: {str(self.id)}'
