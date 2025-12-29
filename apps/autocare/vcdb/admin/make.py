from django.contrib import admin
from apps.autocare.vcdb.models.make import Make
from .base import VCdbModelAdmin


@admin.register(Make)
class MakeAdmin(VCdbModelAdmin):
    """
    VCDB Make reference admin.
    Required for autocomplete usage.
    """

    search_fields = (
        "make_name",
        "make_id",
    )

    list_display = (
        "make_id",
        "make_name",
        "effective_datetime",
        "end_datetime",
    )

    ordering = ("make_name",)
