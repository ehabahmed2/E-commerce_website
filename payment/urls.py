from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment, name='payment'),
    path('checkout', views.checkout, name='checkout'),
    path('billing_info', views.billing_info, name='billing_info'),
    path('process_order', views.process_order, name='process_order'),
]
