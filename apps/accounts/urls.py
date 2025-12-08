"""
URL configuration for the accounts application.
"""
from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('registration-pending/', views.registration_pending_view, name='registration_pending'),
    path('profile/', views.profile_view, name='profile'),
]