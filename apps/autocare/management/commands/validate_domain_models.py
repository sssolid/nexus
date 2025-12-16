from __future__ import annotations

import importlib
import inspect
import re
from pathlib import Path

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from django.db import models


class Command(BaseCommand):
    help = "Validate Autocare domain models for FK/M2M integrity and naming correctness"

    def add_arguments(self, parser):
        parser.add_argument("--db", required=True, help="Database domain (vcdb, pcdb, etc)")

    def handle(self, *args, **opts):
        db = opts["db"]
        base_path = Path(f"apps/autocare/models/{db}")

        if not base_path.exists():
            raise CommandError(f"Models directory not found: {base_path}")

        errors: list[str] = []

        # 1. Import all model modules
        for file in base_path.glob("*.py"):
            if file.name.startswith("_"):
                continue

            module_name = f"apps.autocare.models.{db}.{file.stem}"
            try:
                importlib.import_module(module_name)
            except Exception as exc:
                errors.append(f"Import failed: {module_name} → {exc}")

        # 2. Collect models
        domain_models = [
            m for m in apps.get_models()
            if m.__module__.startswith(f"apps.autocare.models.{db}")
        ]

        model_map = {m.__name__: m for m in domain_models}

        # 3. Validate fields
        for model in domain_models:
            self.stdout.write("Validating " + model.__name__ + " ...")
            for field in model._meta.get_fields():

                # FK validation
                if isinstance(field, models.ForeignKey):
                    target = field.remote_field.model
                    if target not in model_map.values():
                        errors.append(
                            f"{model.__name__}.{field.name} FK target unresolved: {target}"
                        )

                # M2M validation
                if isinstance(field, models.ManyToManyField):
                    through = field.remote_field.through
                    if isinstance(through, str):
                        errors.append(
                            f"{model.__name__}.{field.name} uses string through={through}"
                        )
                    else:
                        if through.__name__ not in model_map:
                            errors.append(
                                f"{model.__name__}.{field.name} through model missing: {through}"
                            )

                    if "_" in through.__name__:
                        errors.append(
                            f"{model.__name__}.{field.name} through model not CamelCase: {through.__name__}"
                        )

        # 4. M2M completeness check
        join_models = [
            m for m in domain_models
            if re.search(r"To[A-Z]", m.__name__)
        ]

        for join in join_models:
            fks = [
                f for f in join._meta.get_fields()
                if isinstance(f, models.ForeignKey)
            ]
            if len(fks) != 2:
                continue

            left, right = fks[0].remote_field.model, fks[1].remote_field.model

            left_m2m = [
                f for f in left._meta.get_fields()
                if isinstance(f, models.ManyToManyField) and f.remote_field.through == join
            ]
            right_m2m = [
                f for f in right._meta.get_fields()
                if isinstance(f, models.ManyToManyField) and f.remote_field.through == join
            ]

            if len(left_m2m) != 1 or len(right_m2m) != 1:
                errors.append(
                    f"Join model {join.__name__} not promoted symmetrically "
                    f"(left={len(left_m2m)}, right={len(right_m2m)})"
                )

        if errors:
            for e in errors:
                self.stderr.write(f"ERROR: {e}")
            raise CommandError(f"Validation failed with {len(errors)} error(s)")

        self.stdout.write(self.style.SUCCESS("Domain model validation PASSED"))
