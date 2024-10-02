from django.contrib import admin
from .models import Category, Customer, Order, Product, Profile
from django.contrib.auth.models import User
# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Profile)

# Mixing User info with Profile info
class ProfileMix(admin.StackedInline):
    model = Profile
    
#extends user Model
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username', 'email', ]
    inlines = [ProfileMix]

# unregister old way
admin.site.unregister(User)

# register with new way
admin.site.register(User, UserAdmin)




