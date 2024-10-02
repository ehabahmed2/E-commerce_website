from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.models import User
from store.models import Product

def payment(request):
    return render(request, 'payment.html', {})

def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_products
    quantities = cart.get_quantities 
    totals = cart.cart_totals()
    
    # address
    if request.user.is_authenticated: # check if current user is logged in
        if not totals:
            messages.error(request, 'Nothing added in cart yet')
            return redirect('home')
        else: 
            try:
                shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
                if ShippingAddress.objects.get(user__id=request.user.id):
                    redirect('billing_info')
            except ShippingAddress.DoesNotExist:
                shipping_user = ShippingAddress(user=request.user)
            
            
            shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
            return render(request, 'checkout.html', {'cart_products': cart_products, 'quantities': quantities, 'totals': totals, 'shipping_form': shipping_form})
    else: 
        messages.error(request, 'Access denied')
        return redirect('login')


def billing_info(request):
    cart = Cart(request)
    cart_products = cart.get_products
    quantities = cart.get_quantities 
    totals = cart.cart_totals()
    # address
    if request.user.is_authenticated: # check if current user is logged in
        if totals == 0:
            messages.error(request, 'Nothing in card to buy')
            return redirect('home')
        else:
            payment_form = PaymentForm() # Get the form we created and pass it over
            # get current shipping info and save it in a session
            shipping_info = request.POST
            request.session['shipping_info'] = shipping_info
            
            return render(request, 'billing_info.html', {'cart_products': cart_products, 'quantities': quantities, 'totals': totals, 'shipping_info': request.POST, 'payment_form': payment_form})
        
    else:
        messages.error(request, 'Access denied')
        return redirect('home')

def process_order(request):
    if request.POST:
        
        cart = Cart(request)
        cart_products = cart.get_products()
        quantities = cart.get_quantities
        totals = cart.cart_totals()
        # get billing info from last page
        payment_form = PaymentForm(request or None)
        # get shipping info that is saved in session
        shipping_info = request.session.get('shipping_info')
        
        # Gather the order info
        full_name = shipping_info['shipping_full_name']
        email = shipping_info['shipping_email']
        amount_paid = totals
        
        # Create a shipping address from shipping info session
        shipping_address = f"{shipping_info['shipping_address1']} \n{shipping_info['shipping_address2']} \n{shipping_info['shipping_city']} \n{shipping_info['shipping_state']} \n{shipping_info['shipping_city']} \n{shipping_info['shipping_country']}\n"
        
        user = request.user
        # Create an order
        create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
        # Save the order
        create_order.save()
        
        # Add order items
        # Get order ID
        order_id = create_order.pk
        # Get product info
        for product in cart_products:
            # get id
            product_id = product.id
            # get product price
            if product.is_sale:
                price = product.sale_price
            else: 
                price = product.price
            # Get quantity
            for key, val in quantities().items():
                if int(key) == product.id:
                    # Create order item
                    create_order_item = OrderItem(order_id=order_id, product_id=product_id, user_id=user.id, quantity=val, price=price) 
                    create_order_item.save()
                
        messages.success(request, 'Payment is processing now')
        return render(request, 'process_order.html', {})
    else:
        messages.error(request, 'Access denied')
        return redirect('home')


