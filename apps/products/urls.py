"""
URL configuration for the products application.
"""
from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_search, name='search'),
    path('customer/', views.customer_catalog, name='customer_catalog'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
]
