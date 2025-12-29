from django.contrib import admin
from apps.autocare.models.vcdb.sub_model import SubModel
from .base import VCdbModelAdmin


@admin.register(SubModel)
class SubModelAdmin(VCdbModelAdmin):
    search_fields = (
        "sub_model_name",
        "submodel_id",
    )

    list_display = (
        "submodel_id",
        "sub_model_name",
        "effective_datetime",
        "end_datetime",
    )

    ordering = ("sub_model_name",)
