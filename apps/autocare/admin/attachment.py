from django.contrib import admin
from apps.autocare.models.vcdb.attachment import Attachment
from .base import VCdbModelAdmin


@admin.register(Attachment)
class AttachmentAdmin(VCdbModelAdmin):
    search_fields = (
        "attachment_file_name",
        "attachment_description",
    )

    list_display = (
        "attachment_file_name",
        "attachment_description",
        "attachment_type_name",
    )

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("attachment_type")
        )

    @admin.display(
        ordering="attachment_type__code_value",
        description="Attachment Type",
    )
    def attachment_type_name(self, obj):
        if obj.attachment_type:
            return f"{obj.attachment_type.code_value} — {obj.attachment_type.code_description}"
        return "-"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "attachment_type":
            kwargs["queryset"] = (
                db_field.remote_field.model.objects
                .filter(reference_fields__pies_field_id=32)
                .distinct()
                .order_by("code_value")
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
