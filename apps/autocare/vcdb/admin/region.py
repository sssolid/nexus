from django.contrib import admin
from apps.autocare.vcdb.models.region import Region
from .base import VCdbModelAdmin


@admin.register(Region)
class RegionAdmin(VCdbModelAdmin):
    search_fields = (
        "region_id",
        "region_name",
    )

    list_display = (
        "region_id",
        "region_name",
    )

    ordering = ("region_name",)
