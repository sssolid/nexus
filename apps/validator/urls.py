"""URL configuration for the validator application."""
from django.urls import path
from . import views

app_name = 'validator'

urlpatterns = [
    path('', views.validator_upload, name='upload'),
]
