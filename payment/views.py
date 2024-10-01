from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django.contrib import messages

# Create your views here.
def payment(request):
    return render(request, 'payment.html', {})

def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_products
    quantities = cart.get_quantities 
    totals = cart.cart_totals()
    
    # address
    if request.user.is_authenticated: # check if current user is logged in
        try:
            shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        except ShippingAddress.DoesNotExist:
            shipping_user = ShippingAddress(user=request.user)
        
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        return render(request, 'checkout.html', {'cart_products': cart_products, 'quantities': quantities, 'totals': totals, 'shipping_form': shipping_form})
    else: 
        messages.error(request, 'You must be logged in to access this page')
        return redirect('login')
    