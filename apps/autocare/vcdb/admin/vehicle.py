from django.contrib import admin
from django.contrib.admin import RelatedOnlyFieldListFilter

from apps.autocare.vcdb.models.vehicle import Vehicle
from apps.autocare.vcdb.models.vehicle_to_class import VehicleToClass


class VehicleToClassInline(admin.TabularInline):
    model = VehicleToClass
    fk_name = "vehicle"

    extra = 0
    show_change_link = True

    autocomplete_fields = ("vehicle_class",)

    readonly_fields = (
        "vehicle_to_class_id",
        "culture_id",
        "effective_datetime",
        "end_datetime",
        "source",
    )

    fields = (
        "vehicle_class",
        "source",
        "effective_datetime",
        "end_datetime",
    )

    can_delete = False

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    """
    VCDB Vehicle admin — corrected for actual schema.
    """

    # =====================================================
    # LIST VIEW
    # =====================================================

    list_display = (
        "vehicle_id",
        "year",
        "make_name",
        "model_name",
        "sub_model_name",
        "region",
        "publication_stage",
    )

    list_select_related = (
        "base_vehicle",
        "base_vehicle__vehicle_year",
        "base_vehicle__make",
        "base_vehicle__vehicle_model",
        "sub_model",
        "region",
        "publication_stage",
    )

    list_filter = (
        ("region", RelatedOnlyFieldListFilter),
        ("publication_stage", RelatedOnlyFieldListFilter),
    )

    ordering = (
        "-base_vehicle__vehicle_year_id",
        "base_vehicle__make_id",
        "base_vehicle__vehicle_model_id",
    )

    autocomplete_fields = (
        "base_vehicle",
        "sub_model",
        "region",
        "publication_stage",
    )

    inlines = (
        VehicleToClassInline,
    )

    list_per_page = 50
    list_max_show_all = 200
    show_full_result_count = False

    # =====================================================
    # SEARCH
    # =====================================================

    search_fields = (
        "vehicle_id",
        "base_vehicle__base_vehicle_id",
        "base_vehicle__make__make_name",
        "base_vehicle__vehicle_model__model_name",
        "sub_model__sub_model_name",
    )

    # =====================================================
    # DETAIL VIEW
    # =====================================================

    raw_id_fields = (
        "base_vehicle",
        "sub_model",
        "region",
        "publication_stage",
    )

    readonly_fields = (
        "vehicle_id",
        "resolved_name"
    )

    fieldsets = (
        (
            "Vehicle Identity",
            {
                "fields": (
                    "base_vehicle",
                    "sub_model",
                    "region",
                )
            },
        ),
        (
            "Publication",
            {
                "fields": (
                    "publication_stage",
                    "publication_stage_source",
                    "publication_stage_date",
                    "source",
                )
            },
        ),
        (
            "System Metadata",
            {
                "fields": (
                    "vehicle_id",
                )
            },
        ),
    )

    # =====================================================
    # VCDB SAFETY
    # =====================================================

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    # =====================================================
    # RESOLVED DISPLAY HELPERS
    # =====================================================

    @admin.display(description="Year", ordering="base_vehicle__vehicle_year__year_id")
    def year(self, obj):
        return obj.base_vehicle.vehicle_year.year_id

    @admin.display(description="Make", ordering="base_vehicle__make_id")
    def make_name(self, obj):
        return obj.base_vehicle.make.make_name

    @admin.display(description="Model", ordering="base_vehicle__vehicle_model_id")
    def model_name(self, obj):
        return obj.base_vehicle.vehicle_model.model_name

    @admin.display(description="Submodel", ordering="sub_model__sub_model_name")
    def sub_model_name(self, obj):
        return obj.sub_model.sub_model_name if obj.sub_model else "—"

    @admin.display(description="Resolved Vehicle Name")
    def resolved_name(self, obj):
        """
        Canonical human-readable VCDB vehicle string.
        """
        parts = [
            str(obj.base_vehicle.vehicle_year.year_id),
            obj.base_vehicle.make.make_name,
            obj.base_vehicle.vehicle_model.model_name,
        ]

        if obj.sub_model:
            parts.append(obj.sub_model.sub_model_name)

        return " ".join(parts)
