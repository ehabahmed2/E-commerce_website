from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User

admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

# create an order item inline
class OrderItmeInline(admin.StackedInline):
    model = OrderItem
    extra = 0


# Extend our order model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ['date_ordered', 'shipped_date']
    inlines = [OrderItmeInline]

# unregister order model
admin.site.unregister(Order)

# Re-register our Order and OrderItem
admin.site.register(Order, OrderAdmin)