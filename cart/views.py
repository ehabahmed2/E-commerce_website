from django.shortcuts import render, get_object_or_404, redirect 
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages



# Create your views here.
def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_products
    quantities = cart.get_quantities 
    totals = cart.cart_totals()
    return render(request, 'summary.html', {'cart_products': cart_products, 'quantities': quantities, 'totals': totals})

# Adding product to cart
def cart_add(request):
    if not request.user.is_authenticated:
        # Return an error response as JSON
        return JsonResponse({'error': 'You must be logged in to add items to the cart.', 'redirect': True})
    
    # Get the cart
    cart = Cart(request)

    # Check if the request is a POST action
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))  
        product_qty = int(request.POST.get('product_qty'))  
        
        product = get_object_or_404(Product, id=product_id)
        # adding the product and quantity
        cart.add(product=product, quantity=product_qty)
        
        # getting card quantity
        cart_quantity = cart.__len__()

        response = JsonResponse({'qty': cart_quantity})
        messages.success(request, "Product added to cart...")

        return response
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


# Delete product from cart
def cart_delete(request):
    cart = Cart(request)
    
    # Check if the request is a POST action
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))  # Get product ID from POST data
        
        # Call the delete function
        cart.delete(product=product_id)
        
        # Return a JSON response with the deleted product ID
        response = JsonResponse({'product': product_id})
        messages.success(request, "Product is deleted now...")

        return response

# Update product quantity in cart
def cart_update(request):
    cart = Cart(request)
    
    # Check if the request is a POST action
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))  # Get product ID from POST data
        quantity = int(request.POST.get('quantity'))  # Get quantity from POST data
        
        # Call the add function to update quantity
        cart.add(product=Product.objects.get(id=product_id), quantity=quantity)
        
        # Return a JSON response
        response = JsonResponse({'product': product_id, 'quantity': quantity})
        messages.success(request, "Product is updated now... ")

        return response

