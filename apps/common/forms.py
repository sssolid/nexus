from django import forms
from django_countries.widgets import CountrySelectWidget
from .models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            "address_line1",
            "address_line2",
            "city",
            "state_province",
            "postal_code",
            "country",
        ]
        widgets = {
            "country": CountrySelectWidget(attrs={"class": "form-control"}),
        }
