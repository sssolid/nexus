from django.contrib import admin
from apps.autocare.vcdb.models.class_ import VehicleClass
from .base import VCdbModelAdmin

@admin.register(VehicleClass)
class VehicleClassAdmin(VCdbModelAdmin):
    search_fields = (
        "class_name",
        "class_id",
    )

    list_display = (
        "class_id",
        "class_name",
    )
