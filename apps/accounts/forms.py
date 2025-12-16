"""
Forms for the accounts application.
"""
from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django_countries.widgets import CountrySelectWidget

from .models import User, UserProfile


class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField(label=_("Email"), max_length=254)
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput)

    error_messages = {
        "invalid_login": _("Please enter a correct email and password."),
        "inactive": _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user_cache = authenticate(
                self.request,
                email=email,
                password=password,
            )
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages["invalid_login"],
                    code="invalid_login",
                )

        return self.cleaned_data

    def get_user(self):
        return self.user_cache


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
            'timezone',
            'notifications_enabled',
            'email_notifications',
            'newsletter_subscription',
            'items_per_page',
            'default_export_format',
        ]
        widgets = {
            'timezone': forms.Select(attrs={'class': 'form-control'}),
        }
