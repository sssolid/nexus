from django.contrib import admin


class VCdbModelAdmin(admin.ModelAdmin):
    """
    Base admin for all VCDB reference tables.

    Enforces search_fields so autocomplete_fields
    can never be misconfigured silently.
    """

    search_fields: tuple[str, ...] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if not cls.search_fields:
            raise ValueError(
                f"{cls.__name__} must define search_fields "
                "because it may be used with autocomplete_fields."
            )

    # Global VCDB defaults
    show_full_result_count = False
    list_per_page = 100

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
