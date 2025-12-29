from django.contrib import admin
from apps.autocare.vcdb.models.publication_stage import PublicationStage
from .base import VCdbModelAdmin


@admin.register(PublicationStage)
class PublicationStageAdmin(VCdbModelAdmin):
    search_fields = (
        "publication_stage_id",
        "publication_stage_name",
    )

    list_display = (
        "publication_stage_id",
        "publication_stage_name",
    )

    ordering = ("publication_stage_name",)
