from django.contrib import admin
from apps.autocare.models.reference.pies_code import AttachmentType
from .base import VCdbModelAdmin


@admin.register(AttachmentType)
class AttachmentTypeAdmin(VCdbModelAdmin):
    """
    Read-only reference view for Attachment / Asset Types (PIESFieldId = 32).
    """

    list_display = (
        "code_value",
        "code_description",
        "code_format",
        "source",
    )

    search_fields = (
        "code_value",
        "code_description",
    )

    ordering = ("code_value",)

    readonly_fields = (
        "pies_code_id",
        "code_value",
        "code_format",
        "field_format",
        "code_description",
        "source",
    )

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .filter(reference_fields__pies_field_id=32)
            .distinct()
        )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
