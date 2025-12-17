from django.contrib import admin
from django.apps import apps

VCDB_APP_LABEL = "autocare"
VCDB_SCHEMA_PREFIX = '"autocare_vcdb".'


class VCdbModelAdmin(admin.ModelAdmin):
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
    Register all Autocare models whose db_table lives in the autocare_vcdb schema.
    This is called lazily and ONLY when AUTOCARE_VCDB_READY=1.
    """
    for model in apps.get_models():
        if model._meta.app_label != VCDB_APP_LABEL:
            continue

        if not str(model._meta.db_table).startswith(VCDB_SCHEMA_PREFIX):
            continue

        try:
            admin.site.register(model, VCdbModelAdmin)
        except admin.sites.AlreadyRegistered:
            pass
