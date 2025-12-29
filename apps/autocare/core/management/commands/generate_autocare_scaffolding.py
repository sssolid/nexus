from pathlib import Path
from django.core.management.base import BaseCommand


BASE_DIR = Path("apps/autocare")


class Command(BaseCommand):
    help = "Generate bootstrap-safe admin, views, and urls scaffolding for Autocare VCDB models."

    def handle(self, *args, **options):
        self.stdout.write("▶ Generating Autocare VCDB scaffolding (bootstrap-safe)")

        self._generate_admin()
        self._generate_views()
        self._generate_urls()

        self.stdout.write(self.style.SUCCESS("✔ Autocare VCDB scaffolding generated"))

    # ------------------------------------------------------------------
    # Admin (GUARDED + LAZY)
    # ------------------------------------------------------------------

    def _generate_admin(self):
        admin_dir = BASE_DIR / "admin"
        admin_dir.mkdir(parents=True, exist_ok=True)

        # __init__.py (guarded)
        (admin_dir / "__init__.py").write_text(
            """\
import os

# Only register VCDB admin when generated models exist
if os.environ.get("AUTOCARE_VCDB_READY") == "1":
    from .vcdb import register_vcdb_models
    register_vcdb_models()
""",
            encoding="utf-8",
        )

        # vcdb.py (NO model imports at module load)
        (admin_dir / "vcdb.py").write_text(
            """\
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
    \"\"\"
    Register all Autocare models whose db_table lives in the autocare_vcdb schema.
    This is called lazily and ONLY when AUTOCARE_VCDB_READY=1.
    \"\"\"
    for model in apps.get_models():
        if model._meta.app_label != VCDB_APP_LABEL:
            continue

        if not str(model._meta.db_table).startswith(VCDB_SCHEMA_PREFIX):
            continue

        try:
            admin.site.register(model, VCdbModelAdmin)
        except admin.sites.AlreadyRegistered:
            pass
""",
            encoding="utf-8",
        )

    # ------------------------------------------------------------------
    # Views (SAFE — no model imports)
    # ------------------------------------------------------------------

    def _generate_views(self):
        views_dir = BASE_DIR / "views"
        views_dir.mkdir(parents=True, exist_ok=True)

        # __init__.py
        (views_dir / "__init__.py").write_text("", encoding="utf-8",)

        (views_dir / "vcdb.py").write_text(
            """\
from django.apps import apps
from django.http import Http404
from django.views.generic import ListView, DetailView


class VCdbModelMixin:
    app_label = "autocare"

    def get_model(self):
        model_name = self.kwargs["model"]
        try:
            return apps.get_model(self.app_label, model_name)
        except LookupError:
            raise Http404(f"Unknown VCDB model: {model_name}")


class VCdbListView(VCdbModelMixin, ListView):
    paginate_by = 50
    template_name = "autocare/vcdb/list.html"

    def get_queryset(self):
        self.model = self.get_model()
        return self.model.objects.all()


class VCdbDetailView(VCdbModelMixin, DetailView):
    template_name = "autocare/vcdb/detail.html"

    def get_object(self):
        self.model = self.get_model()
        return super().get_object()
""",
            encoding="utf-8",
        )

    # ------------------------------------------------------------------
    # URLs (SAFE — no model imports)
    # ------------------------------------------------------------------

    def _generate_urls(self):
        urls_dir = BASE_DIR / "urls"
        urls_dir.mkdir(parents=True, exist_ok=True)

        # __init__.py (guarded)
        (urls_dir / "__init__.py").write_text("", encoding="utf-8", )

        (urls_dir / "vcdb.py").write_text(
            """\
from django.urls import path
from apps.autocare.views.vcdb import VCdbListView, VCdbDetailView


app_name = "autocare_vcdb"

urlpatterns = [
    path("<str:model>/", VCdbListView.as_view(), name="vcdb-list"),
    path("<str:model>/<int:pk>/", VCdbDetailView.as_view(), name="vcdb-detail"),
]
""",
            encoding="utf-8",
        )
