from pathlib import Path
from django.core.management.base import BaseCommand

from apps.autocare.schema.normalizer import safe_identifier
from apps.autocare.schema.parser import parse_schema
from apps.autocare.schema.model_writer import write_model


class Command(BaseCommand):
    help = "Generate Django models from Autocare SQL schema"

    def add_arguments(self, parser):
        parser.add_argument("--schema", required=True)
        parser.add_argument("--db", required=True)

    def handle(self, *args, **opts):
        schema_path = Path(opts["schema"])
        out_dir = Path(f"apps/autocare/models/schema/{opts['db']}")
        out_dir.mkdir(parents=True, exist_ok=True)
        touch_schema_init = Path(f"apps/autocare/models/schema/__init__.py")
        touch_schema_init.touch(exist_ok=True)
        touch_init = Path(f"{out_dir}/__init__.py")
        touch_init.touch(exist_ok=True)

        tables = parse_schema(schema_path)

        for table, meta in tables.items():
            code = write_model(table, meta)
            filename = safe_identifier(table.lower())
            file = out_dir / f"{filename}.py"
            file.write_text(code)

        self.stdout.write(self.style.SUCCESS("Models generated successfully"))
