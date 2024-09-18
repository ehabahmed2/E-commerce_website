from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.


# create a user profile
class Profile(models.Model):
    # Create a user from current user that logged in 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Get time and date (optional)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    governorate = models.CharField(max_length=200, blank=True)
    old_cart = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return self.user.username
    
# Create a user profile func to save profile when sign up
def create_profile(sender, instance, created, **kwargs):
    if created: 
        user_profile = Profile(user=instance)
        user_profile.save()



# Catagories of the product
class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='Categories/imgs/%y/%m/%d/', default='Categories/imgs/default.jpg')
    description = models.TextField(max_length=200 , default='Categories/description')
    def __str__(self):
        return self.name


class Customer(models.Model):
    full_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=11)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    
    def __str__(self):
        return self.full_name


class Product(models.Model):
    product_name = models.CharField(max_length=50)
    price = models.DecimalField(default=0,decimal_places=2 ,max_digits=10)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.TextField(max_length=500, default='', null=True)
    image = models.ImageField(upload_to='Products/imgs/%y/%m/%d/')
    
    #adding for sale
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0,decimal_places=2 ,max_digits=10)
    def __str__(self):
        return self.product_name
    
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default='', blank=True)
    phone = models.CharField(max_length=11, default='', blank=True)
    date = models.DateField(default=datetime.datetime.now)
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return self.product
