"""URL configuration for the ACES/PIES application."""
from django.urls import path
from . import views

app_name = 'aces_pies'

urlpatterns = [
    path('search/', views.vehicle_search, name='vehicle_search'),
]
