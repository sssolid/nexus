from django.contrib import admin
from django.apps import apps

VCDB_APP_LABEL = "autocare"
VCDB_SCHEMA_PREFIX = '"autocare_vcdb".'

# Models that MUST have explicit admins
SKIP_MODEL_NAMES = {
    "Vehicle",
    "VehicleModel",
    "BaseVehicle",
    "Make",
    "SubModel",
    "Region",
    "PublicationStage",
}


class VCdbModelAdmin(admin.ModelAdmin):
    """
    Fallback admin for simple VCDB reference tables.
    """

    list_per_page = 50
    save_on_top = True

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


def register_vcdb_models():
    """
    Register ALL autocare_vcdb tables that do NOT already have
    a dedicated ModelAdmin.

    Explicit admins always take precedence.
    """

    for model in apps.get_models():

        # Only autocare app
        if model._meta.app_label != VCDB_APP_LABEL:
            continue

        # Only VCDB schema
        if not str(model._meta.db_table).startswith(VCDB_SCHEMA_PREFIX):
            continue

        # Skip models that must be explicitly registered
        if model.__name__ in SKIP_MODEL_NAMES:
            continue

        # Skip if already registered
        if model in admin.site._registry:
            continue

        admin.site.register(model, VCdbModelAdmin)
