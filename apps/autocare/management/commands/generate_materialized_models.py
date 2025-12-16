from pathlib import Path
import re

from django.core.management.base import BaseCommand

from apps.autocare.models.base import (
    AutocareTemporalModel,
    AutocareNamedModel,
)

BASE_TEMPORAL_DB_COLS = {"CultureID", "EffectiveDateTime", "EndDateTime"}
BASE_NAMED_DB_COLS = BASE_TEMPORAL_DB_COLS | {"Name", "MakeName", "ModelName"}


class Command(BaseCommand):
    help = "Promote generated schema models to managed Django domain models"

    def add_arguments(self, parser):
        parser.add_argument("--db", required=True)
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **opts):
        db = opts["db"]
        dry = opts["dry_run"]

        model_dir = Path(f"apps/autocare/models/{db}")

        if not model_dir.exists():
            self.stderr.write(f"Model dir not found: {model_dir}")
            return

        count = 0

        for file in model_dir.glob("*.py"):
            if file.name == "__init__.py":
                continue

            text = file.read_text()

            # 1️⃣ Flip managed = False → True
            text, managed_changes = re.subn(
                r"managed\s*=\s*False",
                "managed = True",
                text,
            )

            # 2️⃣ Detect DB columns
            db_cols = set(re.findall(r'db_column="([^"]+)"', text))

            # 3️⃣ Determine base inheritance
            if BASE_NAMED_DB_COLS.issubset(db_cols):
                base = "AutocareNamedModel"
            elif BASE_TEMPORAL_DB_COLS.issubset(db_cols):
                base = "AutocareTemporalModel"
            else:
                base = None

            # 4️⃣ Inject base inheritance ONLY if needed
            if base and base not in text:
                text = text.replace(
                    "class ",
                    f"from apps.autocare.models.base import {base}\n\nclass ",
                    1,
                )
                text = re.sub(
                    r"class (\w+)\(models.Model\):",
                    rf"class \1({base}):",
                    text,
                )

            if not dry:
                file.write_text(text)

            count += 1

        self.stdout.write(
            self.style.SUCCESS(f"Promoted {count} generated models")
        )
