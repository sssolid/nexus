"""
Forms for the accounts application.
"""
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User, UserProfile


class UserLoginForm(AuthenticationForm):
    """Custom login form using email instead of username."""
    
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
            'autofocus': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )


class UserRegistrationForm(UserCreationForm):
    """Form for customer registration."""
    
    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'last_name',
            'company_name', 'phone_number', 'password1', 'password2'
        ]
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        """Set user_type to CUSTOMER for registration."""
        super().__init__(*args, **kwargs)
        self.instance.user_type = User.UserType.CUSTOMER


class UserProfileForm(forms.ModelForm):
    """Form for editing user profile."""
    
    class Meta:
        model = UserProfile
        fields = [
            'address_line1', 'address_line2', 'city', 'state',
            'postal_code', 'country', 'notifications_enabled',
            'email_notifications', 'newsletter_subscription',
            'items_per_page', 'default_export_format'
        ]
        widgets = {
            'address_line1': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line2': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
        }
