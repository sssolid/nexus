from __future__ import annotations

from dataclasses import dataclass
from typing import List

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import connection
from django.db.models import ForeignKey


@dataclass(frozen=True)
class Issue:
    level: str  # "ERROR" | "WARN"
    model: str
    message: str


class Command(BaseCommand):
    help = "Validate generated autocare models. DB checks are optional."

    def add_arguments(self, parser):
        parser.add_argument("--app-label", default="autocare")
        parser.add_argument("--schema", default="autocare_vcdb")
        parser.add_argument(
            "--check-db",
            action="store_true",
            help="Also verify that db_table exists in the database (only after you have created those tables).",
        )

    def handle(self, *args, **opts):
        app_label: str = opts["app_label"]
        schema: str = opts["schema"]
        check_db: bool = bool(opts["check_db"])

        issues: List[Issue] = []

        # Ensure vcdb package imports cleanly
        try:
            __import__("apps.autocare.models.vcdb", fromlist=["*"])
        except Exception as e:
            issues.append(Issue("ERROR", "vcdb", f"Failed to import generated vcdb package: {e!r}"))
            self._print_and_exit(issues)

        models = [m for m in apps.get_models() if m._meta.app_label == app_label and "." in m._meta.db_table]
        if not models:
            issues.append(Issue("WARN", "all", "No models found with schema-qualified db_table."))
            self._print_and_exit(issues)

        # Optional DB table existence checks
        db_tables = set()
        if check_db:
            db_tables = set(self._get_tables(schema=schema))

        for model in models:
            model_label = f"{model.__module__}.{model.__name__}"
            full_table = model._meta.db_table

            # Always validate index field names exist on the model
            for idx in model._meta.indexes:
                for field_name in idx.fields:
                    if field_name not in {f.name for f in model._meta.fields}:
                        issues.append(Issue("ERROR", model_label, f"Index references missing field: {field_name!r}"))

            # Validate FK targets resolve
            for field in model._meta.fields:
                if isinstance(field, ForeignKey):
                    if field.remote_field.model is None:
                        issues.append(Issue("ERROR", model_label, f"ForeignKey {field.name!r} has unresolved target model."))

            # Only check DB existence if requested
            if check_db:
                if not full_table.startswith(schema + "."):
                    continue
                table = full_table.split(".", 1)[1]
                if table not in db_tables:
                    issues.append(Issue("ERROR", model_label, f"Table not found in DB: {schema}.{table}"))

        self._print_and_exit(issues)

    def _get_tables(self, schema: str) -> List[str]:
        with connection.cursor() as cur:
            cur.execute(
                """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = %s
                ORDER BY table_name;
                """,
                [schema],
            )
            return [r[0] for r in cur.fetchall()]

    def _print_and_exit(self, issues: List[Issue]) -> None:
        errors = [i for i in issues if i.level == "ERROR"]
        warns = [i for i in issues if i.level == "WARN"]

        for i in warns:
            self.stdout.write(self.style.WARNING(f"[WARN] {i.model}: {i.message}"))
        for i in errors:
            self.stdout.write(self.style.ERROR(f"[ERROR] {i.model}: {i.message}"))

        if errors:
            raise SystemExit(1)

        self.stdout.write(self.style.SUCCESS("✔ Validation passed."))
