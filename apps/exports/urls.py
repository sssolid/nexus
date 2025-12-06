"""URL configuration for the exports application."""
from django.urls import path
from . import views

app_name = 'exports'

urlpatterns = [
    path('', views.export_list, name='export_list'),
    path('create/', views.export_form, name='export_form'),
]
