from django.db import models
from django_countries.fields import CountryField

class Address(models.Model):
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)

    country = CountryField(default="US")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.address_line1}, {self.city}, {self.country}"
