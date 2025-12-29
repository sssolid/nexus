from django.contrib import admin
from apps.autocare.models.vcdb.model import VehicleModel


@admin.register(VehicleModel)
class VehicleModelAdmin(admin.ModelAdmin):
    """
    VCDB VehicleModel admin.

    Required for autocomplete_fields usage.
    Read-only, search-optimized.
    """

    # =====================================================
    # LIST VIEW
    # =====================================================

    list_display = (
        "model_id",
        "model_name",
        "vehicle_type",
        "effective_datetime",
        "end_datetime",
    )

    list_select_related = (
        "vehicle_type",
    )

    ordering = (
        "model_name",
        "model_id",
    )

    list_per_page = 100
    show_full_result_count = False

    # =====================================================
    # SEARCH (REQUIRED FOR AUTOCOMPLETE)
    # =====================================================

    search_fields = (
        "model_name",
        "model_id",
    )

    # =====================================================
    # DETAIL VIEW
    # =====================================================

    raw_id_fields = (
        "vehicle_type",
    )

    readonly_fields = (
        "model_id",
        "culture_id",
        "effective_datetime",
        "end_datetime",
    )

    fieldsets = (
        (
            "Model Identity",
            {
                "fields": (
                    "model_id",
                    "model_name",
                    "vehicle_type",
                )
            },
        ),
        (
            "Autocare Metadata",
            {
                "fields": (
                    "culture_id",
                    "effective_datetime",
                    "end_datetime",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    # =====================================================
    # SAFETY
    # =====================================================

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
