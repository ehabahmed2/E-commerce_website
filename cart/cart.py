from store.models import Product, Profile


class Cart:
    def __init__(self, request):
        self.session = request.session
        # get the request
        self.request = request
        cart = self.session.get('cart')
        if not cart:
            # Save an empty cart in the session if it doesn't exist
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        
        if product_id in self.cart:
            # Update its qty
            self.cart[product_id] = int(product_qty)
        else:
            self.cart[product_id] = int(product_qty)
        self.session.modified = True
        # Get current user
        current_user = Profile.objects.filter(user__id=self.request.user.id)
        # convert current id {'3': 1, '4': 2} to something like this {"3":1, "4", 2} as json workds with double quotations only
        json_cart = str(self.cart)
        json_cart = json_cart.replace("\'","\"")
        # Save this into Profile model
        current_user.update(old_cart=str(json_cart))
    
    # To add the products again after logging in
    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
        
        if product_id in self.cart:
            # Update its qty
            self.cart[product_id] = int(product_qty)
        else:
            self.cart[product_id] = int(product_qty)
        self.session.modified = True
        
    # To check length of carts
    def __len__(self):
        return len(self.cart)
    
    # Get products to show in summary page
    def get_products(self):
        # getting ids from carts
        product_ids = self.cart.keys()
        # use ids to look up products in database
        products = Product.objects.filter(id__in=product_ids) 
        return products
    
    # Get number of items
    def get_quantities(self):
        quantities = self.cart
        return quantities
    
    # Delete Function in cart.py
    def delete(self, product):
        product_id = str(product)  # Convert product_id to string
        # Delete from dictionary
        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True
            
            # Get current user
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # convert current id {'3': 1, '4': 2} to something like this {"3":1, "4", 2} as json workds with double quotations only
            json_cart = str(self.cart)
            json_cart = json_cart.replace("\'","\"")
            # Save this into Profile model
            current_user.update(old_cart=str(json_cart))
        else:
            print('Product not found in cart')

    def cart_totals(self):
        # quantities (getting ids and val like this == {'1', 2}) key and val
        quantities = self.cart
        # get id from cart
        product_ids = self.cart.keys()
        # save ids to our database model
        products = Product.objects.filter(id__in=product_ids)
        # loop through product kesy
        total = 0
        for key, val in quantities.items():
            # converting key string to int as we'll caculate it
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * val)
                    else:
                        total = total + (product.price * val)
        return total
    




