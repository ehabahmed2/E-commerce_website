from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegisterUser, UpdateUserForm, UpdatePassword


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
            login(request, user)  # Automatically log in the user
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}!")
            return redirect('home')  # Redirect to home or another page after registration
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