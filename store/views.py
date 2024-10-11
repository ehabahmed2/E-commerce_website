from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegisterUser, UpdateUserForm, UpdatePassword, UserInfoForm

from django.http import HttpResponse
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django.db.models import Q
from cart.cart import Cart
import json

# Create your views here.
#product page
def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product/product.html', {'product': product})

# Categories
def category(request, sk):
    # dealing with hyphens
    sk = sk.replace('-', ' ')
    
    try:
        category = Category.objects.get(name=sk)
        products = Product.objects.filter(category=category)
        return render(request, 'product/category.html', {'products': products, 'category': category})
    except:
        messages.error('That category doesn\'t exist... ')
        return redirect('home')

# Category Summary
def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'product/category_summary.html', {'categories': categories})

# Main Home page
def store(request):
    products = Product.objects.all()
    return render(request, 'home/index.html', context={'products': products})

# about page
def about(request):
    return render(request, 'about/about.html', context={})

# Login and out 
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            
            try:
                # add the items to cart
                # get current user profile
                current_user = Profile.objects.get(user__id=request.user.id)
                # get their saved cart from database
                saved_cart = current_user.old_cart
                #convert database string to a dictionary
                if saved_cart:
                    converted_cart = json.loads(saved_cart)
                    # Add loaded cart dic to our session
                    cart = Cart(request)
                    # loop through item and add items to db
                    for key, val in converted_cart.items():
                        cart.db_add(product=key, quantity=val)
            except:
                pass
            messages.success(request, "You're logged in!")
            return redirect('home')
        else: 
            messages.error(request, "Failed to login...")
            return redirect('login')
    else:
        return render(request, 'users/login.html')

def logout_user(request):
    logout(request)
    messages.success(request, "You're logged out now")
    return redirect('home')

#Register
def register_user(request):
    if request.method == 'POST':
        form = RegisterUser(request.POST)
        if form.is_valid():
            user = form.save()  # The UserCreationForm automatically saves the hashed password
            Profile.objects.create(user=user)  # Create a profile for the new user
            login(request, user)  # Automatically log in the user
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}, Kindly complete the User's info!")
            return redirect('update_info')  # Redirect to home or another page after registration
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterUser()
        messages.info(request, 'not post')
    return render(request, 'users/register.html', {'form': form})

# Update user profile
def update_user(request):
    if request.user.is_authenticated: # check if current user is logged in
        current_user = User.objects.get(id=request.user.id) # get current user unique id
        user_form = UpdateUserForm(request.POST or None, instance=current_user) # get the form for the user (using their id)
        if user_form.is_valid():
            user_form.save()
            login(request, current_user) # to log the user in again after saving info
            messages.success(request, "Your details are saved successfully!")
            return redirect('home')
        return render(request, 'users/update_user.html', {'user_form': user_form})
    messages.error(request, "You must be logged first!")
    return redirect('login')

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        # did they fill in the form
        if request.method == 'POST':
            # get the form 
            form = UpdatePassword(current_user, request.POST)
            # is form valid 
            if form.is_valid():
                form.save()
                messages.success(request, 'Password has been updated!')
                login(request, current_user)
                return redirect('home')
            else: 
                # return a msg with error
                for error in list(form.errors.values()):
                    messages.error(request, error )
                    return redirect('update_password')
                
        else:
            form = UpdatePassword(current_user, request.POST)
            return render(request, 'users/update_password.html', {'password_form': form})
    else:
        messages.error(request, 'You must be logged in first!!')
        return redirect('login')

# Updating user other information
from django.core.exceptions import ObjectDoesNotExist

def update_info(request): 
    if request.user.is_authenticated:  # check if current user is logged in
        try:
            current_user = Profile.objects.get(user__id=request.user.id)  # get current user unique id to match the user's id
        except Profile.DoesNotExist:
            current_user = Profile(user=request.user)
            current_user.save()
        
        # Get current user's shipping info or create a new one if it doesn't exist
        try:
            shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        except ShippingAddress.DoesNotExist:
            shipping_user = ShippingAddress(user=request.user)
        
        # get original user form
        form = UserInfoForm(request.POST or None, instance=current_user)  # get the form for the user (using their id)
        # get shipping form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        # Print the shipping user ID for debugging
        print(f"Shipping ID: {shipping_user.id}")
        
        if form.is_valid() and shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request, "Your details are saved successfully!")
            return redirect('home')
        return render(request, 'users/update_info.html', {'form': form, 'shipping_form': shipping_form})
    messages.error(request, "You must be logged in first!")
    return redirect('update_info')


def search(request):
    if request.method == 'GET':
        searched = request.GET['searched']
        searched = Product.objects.filter(Q(product_name__icontains=searched) | Q(description__icontains=searched))
        if not searched:
            messages.info(request, 'No results found!')
        return render(request, 'product/search.html', {'searched': searched})
    else:
        return render(request, 'product/search.html', {})


