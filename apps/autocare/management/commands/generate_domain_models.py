from __future__ import annotations

import shutil
from pathlib import Path
from collections import Counter

from django.core.management.base import BaseCommand
from django.db import models

from apps.autocare.schema.parser import parse_schema
from apps.autocare.schema.normalizer import (
    camel_to_snake,
    safe_identifier,
    is_reserved_identifier,
)
from apps.autocare.models.base import (
    AutocareTemporalModel,
    AutocareNamedModel,
)
from apps.autocare.models.base import AutocareRawRecord


TEMPORAL_KEYS = {"EffectiveDateTime", "EndDateTime"}


def pascal(name: str) -> str:
    return "".join(p.capitalize() for p in camel_to_snake(name).split("_"))


def safe_class_name(table: str) -> str:
    base = pascal(table)
    if is_reserved_identifier(base.lower()):
        return f"{base}Model"
    return base


def infer_payload_keys(*, source_db: str, endpoint: str) -> set[str]:
    """
    Infer payload keys by finding the newest raw record for this db+endpoint.

    Handles:
    - endpoint stored as "/vcdb/Vehicle"
    - endpoint stored as "/api/v1/vcdb/Vehicle"
    - payload stored as a list of rows
    - payload stored as {"data": [...]} / {"items":[...]} / {"results":[...]}
    """
    def normalize(e: str) -> str:
        e = e.strip()
        # strip api prefix if present
        if e.startswith("/api/v1"):
            e = e[len("/api/v1"):]
        return e

    candidates = {
        normalize(endpoint),
        normalize("/api/v1" + endpoint),
    }

    # try exact match first
    rec = (
        AutocareRawRecord.objects
        .filter(source_db=source_db, endpoint__in=candidates)
        .order_by("-fetched_at")
        .first()
    )
    if not rec:
        return set()

    payload = rec.payload

    # list payload
    if isinstance(payload, list) and payload:
        first = payload[0]
        return set(first.keys()) if isinstance(first, dict) else set()

    # wrapper payload
    if isinstance(payload, dict):
        for k in ("data", "items", "results"):
            v = payload.get(k)
            if isinstance(v, list) and v:
                first = v[0]
                return set(first.keys()) if isinstance(first, dict) else set()

        # single-object payload
        return set(payload.keys())

    return set()


class Command(BaseCommand):
    help = "Generate FINAL domain models from SQL schema + raw payloads"

    def add_arguments(self, parser):
        parser.add_argument("--db", required=True, choices=["vcdb", "pcdb", "padb", "qdb"])
        parser.add_argument("--schema", required=True)
        parser.add_argument("--overwrite", action="store_true")

    def handle(self, *args, **opts):
        db = opts["db"]
        schema_path = Path(opts["schema"]).resolve()
        out_dir = Path(f"apps/autocare/models/{db}")

        if opts["overwrite"] and out_dir.exists():
            shutil.rmtree(out_dir)

        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "__init__.py").touch(exist_ok=True)

        schema = parse_schema(schema_path)
        generated = 0

        for table, meta in schema.items():
            endpoint = f"/{db}/{table}"
            payload_keys = infer_payload_keys(source_db=db, endpoint=f"/{db}/{table}")

            code = self.render_model(
                table=table,
                meta=meta,
                payload_keys=payload_keys,
                db=db,
            )

            file = out_dir / f"{camel_to_snake(table)}.py"
            file.write_text(code)
            generated += 1

        self.stdout.write(self.style.SUCCESS(f"Generated {generated} domain models"))

    # ------------------------------------------------------------------

    def render_model(self, *, table: str, meta: dict, payload_keys: set[str], db: str) -> str:
        columns = meta["columns"]
        pk_cols = meta.get("pk", [])
        fks = meta.get("fks", [])

        # ---- inheritance decision (RAW DATA DRIVEN) ----
        is_temporal = TEMPORAL_KEYS.issubset(payload_keys)
        name_fields = [k for k in payload_keys if k.endswith("Name")]

        if is_temporal and len(name_fields) == 1:
            base = "AutocareNamedModel"
        elif is_temporal:
            base = "AutocareTemporalModel"
        else:
            base = "models.Model"

        class_name = safe_class_name(table)

        lines = [
            "from django.db import models",
            "from apps.autocare.models.base import AutocareTemporalModel, AutocareNamedModel",
            "",
            f"class {class_name}({base}):",
            '    """FINAL DOMAIN MODEL — AUTO-GENERATED"""',
            "",
        ]

        fk_by_col = {fk["column"]: fk for fk in fks}

        for col, col_meta in columns.items():
            sql_type = col_meta["type"]
            nullable = col_meta["nullable"]

            # skip inherited temporal fields
            if base in {"AutocareTemporalModel", "AutocareNamedModel"} and col in TEMPORAL_KEYS:
                continue

            # map Name field if using AutocareNamedModel
            if base == "AutocareNamedModel" and col.endswith("Name"):
                max_len = self.varchar_len(sql_type) or 255
                lines.append(
                    f'    name = models.CharField(max_length={max_len}, db_column="{col}")'
                )
                continue

            # ForeignKey promotion
            if col in fk_by_col:
                fk = fk_by_col[col]
                rel = safe_identifier(col[:-2] if col.endswith("ID") else col)
                ref = safe_class_name(fk["ref_table"])
                lines.append(
                    f'    {rel} = models.ForeignKey("{ref}", db_column="{col}", '
                    f'on_delete=models.DO_NOTHING, related_name="+")'
                )
                continue

            # scalar
            field, kwargs = self.scalar(sql_type, nullable)
            kwargs.append(f'db_column="{col}"')
            if len(pk_cols) == 1 and col == pk_cols[0]:
                kwargs.append("primary_key=True")

            lines.append(f"    {safe_identifier(col)} = {field}({', '.join(kwargs)})")

        lines += [
            "",
            "    class Meta:",
            f'        db_table = "autocare_{db}.{camel_to_snake(table)}"',
            "        managed = True",
        ]

        if len(pk_cols) > 1:
            fields = [safe_identifier(c) for c in pk_cols]
            lines += [
                "        constraints = [",
                f"            models.UniqueConstraint(fields={fields!r}, name='uniq_{camel_to_snake(table)}_pk'),",
                "        ]",
            ]

        return "\n".join(lines)

    # ------------------------------------------------------------------

    def varchar_len(self, sql_type: str) -> int | None:
        if "(" in sql_type:
            try:
                return int(sql_type.split("(")[1].split(")")[0])
            except Exception:
                return None
        return None

    def scalar(self, sql_type: str, nullable: bool):
        st = sql_type.upper()
        kwargs = []
        if "VARCHAR" in st:
            field = "models.CharField"
            kwargs.append(f"max_length={self.varchar_len(st) or 255}")
        elif st in {"INT", "INTEGER"}:
            field = "models.IntegerField"
        elif st == "BIGINT":
            field = "models.BigIntegerField"
        elif "DECIMAL" in st or "NUMERIC" in st:
            field = "models.DecimalField"
            kwargs += ["max_digits=10", "decimal_places=2"]
        elif "TIMESTAMP" in st:
            field = "models.DateTimeField"
        elif st == "DATE":
            field = "models.DateField"
        elif st in {"BOOL", "BOOLEAN"}:
            field = "models.BooleanField"
        else:
            field = "models.TextField"

        if nullable:
            kwargs += ["null=True", "blank=True"]

        return field, kwargs
