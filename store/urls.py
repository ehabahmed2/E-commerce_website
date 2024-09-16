from django.urls import path
from . import views
from .views import register_user

urlpatterns = [
    path('', views.store, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', register_user, name='register_user'),
    path('product/<int:pk>/', views.product, name='product'),
    path('category/<str:sk>/', views.category, name='category'),
    path('category_summary/', views.category_summary, name='category_summary'),
    path('update_user/', views.update_user, name='update_user'),
]
