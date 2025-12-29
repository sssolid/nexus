from django.contrib import admin
from apps.autocare.models.vcdb.aspiration import Aspiration
from .base import VCdbModelAdmin


@admin.register(Aspiration)
class AspirationAdmin(VCdbModelAdmin):
    search_fields = (
        "aspiration_id",
        "aspiration_name",
    )

    list_display = (
        "aspiration_id",
        "aspiration_name",
    )
