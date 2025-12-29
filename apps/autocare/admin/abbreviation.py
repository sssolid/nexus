from django.contrib import admin
from apps.autocare.models.vcdb.abbreviation import Abbreviation
from .base import VCdbModelAdmin


@admin.register(Abbreviation)
class AbbreviationAdmin(VCdbModelAdmin):
    search_fields = (
        "abbreviation",
        "description",
        "long_description"
    )

    list_display = (
        "abbreviation",
        "description",
        "long_description",
    )
