from django.contrib import admin
from apps.autocare.models.vcdb.base_vehicle import BaseVehicle
from .base import VCdbModelAdmin


@admin.register(BaseVehicle)
class BaseVehicleAdmin(VCdbModelAdmin):
    search_fields = (
        "base_vehicle_id",
    )

    list_display = (
        "base_vehicle_id",
        "vehicle_year",
        "make",
        "vehicle_model",
    )

    list_select_related = (
        "vehicle_year",
        "make",
        "vehicle_model",
    )
