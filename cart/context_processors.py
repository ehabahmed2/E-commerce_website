from .cart import Cart

#Creating a context processors so our cart we created can work on all pages
def cart(request):
    # Return default data from our cart.py we created
    return {'cart': Cart(request)}