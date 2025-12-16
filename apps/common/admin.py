from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Address

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "address_line1",
        "city",
        "state_province",
        "country",
        "postal_code",
    )

    list_filter = ("country",)
    search_fields = (
        "address_line1",
        "city",
        "state_province",
        "postal_code",
    )
