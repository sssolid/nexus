from __future__ import annotations

import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from django.core.management.base import BaseCommand

from apps.autocare.schema.parser import parse_schema
from apps.autocare.schema.normalizer import camel_to_snake, safe_identifier, is_reserved_identifier


# ----------------------------
# Helpers / Specs
# ----------------------------

@dataclass
class SqlTable:
    name: str
    columns: dict[str, dict]   # { "MakeID": {"type": "INT", "nullable": False}, ... }
    pk: list[str]
    fks: list[dict]            # [{"column": "...", "ref_table": "...", "ref_column":"..."}]


@dataclass
class ApiModel:
    name: str
    props: dict[str, dict]     # swagger property schema objects


def pascal_case(s: str) -> str:
    return "".join(part.capitalize() for part in s.split("_") if part)


def safe_class_name(raw: str) -> str:
    base = pascal_case(camel_to_snake(raw))
    if is_reserved_identifier(base.lower()):
        return f"{base}Model"
    return base


def unwrap_payload_schema(prop: dict) -> dict:
    # OAS sometimes uses nullable or oneOf etc; we keep it simple.
    return prop or {}


def swagger_type_to_django(prop: dict) -> tuple[str, dict[str, Any]]:
    """
    Map OpenAPI property schema => (FieldClass, kwargs)
    We prefer swagger here because this is "ready to ingest API data".
    SQL will override lengths where available.
    """
    prop = unwrap_payload_schema(prop)
    t = (prop.get("type") or "").lower()
    fmt = (prop.get("format") or "").lower()
    nullable = bool(prop.get("nullable", False))

    kwargs: dict[str, Any] = {}
    if nullable:
        kwargs["null"] = True
        kwargs["blank"] = True

    if t == "integer":
        if fmt == "int64":
            return "models.BigIntegerField", kwargs
        return "models.IntegerField", kwargs

    if t == "number":
        # best effort
        kwargs.setdefault("max_digits", 18)
        kwargs.setdefault("decimal_places", 6)
        return "models.DecimalField", kwargs

    if t == "boolean":
        return "models.BooleanField", kwargs

    if t == "string":
        if fmt in {"date-time", "datetime"}:
            return "models.DateTimeField", kwargs
        if fmt == "date":
            return "models.DateField", kwargs

        # swagger may provide maxLength
        max_len = prop.get("maxLength")
        if isinstance(max_len, int) and max_len > 0:
            kwargs["max_length"] = max_len
            return "models.CharField", kwargs

        # default string
        kwargs["max_length"] = 255
        return "models.CharField", kwargs

    # arrays/objects => JSONField fallback (keeps ingestion safe)
    if t in {"object", "array"}:
        return "models.JSONField", kwargs

    # unknown fallback
    return "models.TextField", kwargs


def sql_type_override(sql_type: str) -> tuple[str | None, dict[str, Any]]:
    """
    SQL is authoritative for max_length / numeric precision where present.
    Returns (FieldClass or None if no override, extra_kwargs)
    """
    st = sql_type.strip().upper()

    # VARCHAR(n)
    m = re.match(r"VARCHAR\((\d+)\)", st)
    if m:
        return "models.CharField", {"max_length": int(m.group(1))}

    # CHAR(n)
    m = re.match(r"CHAR\((\d+)\)", st)
    if m:
        return "models.CharField", {"max_length": int(m.group(1))}

    # numeric(p,s)
    m = re.match(r"(NUMERIC|DECIMAL)\((\d+)\s*,\s*(\d+)\)", st)
    if m:
        return "models.DecimalField", {"max_digits": int(m.group(2)), "decimal_places": int(m.group(3))}

    # timestamps
    if "TIMESTAMP" in st or st in {"DATETIME", "TIMESTAMPTZ"}:
        return "models.DateTimeField", {}

    if st == "DATE":
        return "models.DateField", {}

    if st in {"INT", "INTEGER"}:
        return "models.IntegerField", {}

    if st == "BIGINT":
        return "models.BigIntegerField", {}

    if st in {"BOOL", "BOOLEAN"}:
        return "models.BooleanField", {}

    if st == "TEXT":
        return "models.TextField", {}

    return None, {}


def normalize_endpoint_path(db: str, endpoint: str) -> str:
    """
    endpoint in swagger paths: /api/v1/vcdb/Make
    your ingestion endpoints:   /vcdb/Make
    table name: Make
    """
    endpoint = endpoint.strip()
    endpoint = endpoint.replace("/api/v1/", "/")  # /vcdb/Make
    endpoint = endpoint.lstrip("/")
    parts = endpoint.split("/")
    # expected: ["vcdb", "Make"] or ["vcdb","equipment","Aspiration"]
    if not parts:
        return ""
    if parts[0].lower() != db.lower():
        return ""
    # table name is last segment
    return parts[-1]


def load_openapi_models(openapi_path: Path) -> dict[str, ApiModel]:
    """
    Returns dict: TableName => ApiModel(properties)
    We pick up models from components.schemas and map to a "table name" using heuristics:
      - If schema name ends with XxxClientApiModel => table Xxx
      - Else use last segment after '.' and strip ClientApiModel suffix if present
    """
    doc = json.loads(openapi_path.read_text())
    schemas = (doc.get("components") or {}).get("schemas") or {}

    out: dict[str, ApiModel] = {}
    for full_name, schema in schemas.items():
        props = (schema or {}).get("properties") or {}
        if not props:
            continue

        last = full_name.split(".")[-1]
        # strip common suffixes
        for suf in ("ClientApiModel", "ClientAPIModel", "ApiModel", "Model"):
            if last.endswith(suf):
                last = last[: -len(suf)]
                break

        table = last
        out[table] = ApiModel(name=table, props=props)

    return out


def infer_join_table(sql: SqlTable) -> tuple[str, str] | None:
    """
    Detect join table for M2M:
      - exactly 2 foreign keys
      - mostly consists of those 2 FK cols plus optional Source/temporal metadata plus an ID PK
    Returns (A_table, B_table) if join candidate.
    """
    if len(sql.fks) != 2:
        return None

    fk_cols = {fk["column"] for fk in sql.fks}
    non_meta = set(sql.columns.keys()) - fk_cols
    # allow these non-FK columns in join tables
    allowed = {"Source", "CultureID", "EffectiveDateTime", "EndDateTime"}
    non_meta = {c for c in non_meta if c not in allowed}

    # allow surrogate pk like VehicleToBedConfigID
    # if non_meta is empty or only pk col(s), treat as join
    pk_set = set(sql.pk)
    remainder = non_meta - pk_set

    if remainder:
        return None

    a = sql.fks[0]["ref_table"]
    b = sql.fks[1]["ref_table"]
    return a, b


# ----------------------------
# Writer
# ----------------------------

class ModelWriter:
    def __init__(self, db: str, sql_tables: dict[str, SqlTable], api_models: dict[str, ApiModel]):
        self.db = db
        self.sql_tables = sql_tables
        self.api_models = api_models

    def build(self) -> str:
        lines: list[str] = []
        lines.append("from __future__ import annotations")
        lines.append("")
        lines.append("from django.db import models")
        lines.append("")
        lines.append("# FINAL API-INGEST MODELS (Swagger + SQL merged)")
        lines.append("# Generated by: manage.py generate_api_models")
        lines.append("")

        # First pass: emit all models (including join tables) with FK promotion
        for table in sorted(self.sql_tables.keys()):
            lines.extend(self.render_table_model(self.sql_tables[table]))
            lines.append("")

        # Second pass: emit ManyToMany fields by monkey-patching class attributes at bottom
        # This avoids import-order issues and file naming issues.
        m2m_lines = self.render_m2m()
        if m2m_lines:
            lines.append("# ---- Many-to-Many wiring (through join tables) ----")
            lines.extend(m2m_lines)
            lines.append("")

        return "\n".join(lines).rstrip() + "\n"

    def render_table_model(self, sql: SqlTable) -> list[str]:
        table = sql.name
        class_name = safe_class_name(table)

        api = self.api_models.get(table)
        api_props = api.props if api else {}

        fk_by_col = {fk["column"]: fk for fk in sql.fks}

        out: list[str] = []
        out.append(f"class {class_name}(models.Model):")
        out.append('    """AUTO-GENERATED — READY FOR API INGEST"""')
        out.append("")

        # Merge columns: Swagger is “payload truth”, SQL is “db constraint truth”
        # We want ALL swagger fields (even if not in SQL) because you explicitly asked for that.
        all_cols = list(sql.columns.keys())
        for swagger_col in api_props.keys():
            if swagger_col not in sql.columns:
                all_cols.append(swagger_col)

        # fields
        for col in all_cols:
            # FK promotion only if the column is in SQL fks
            if col in fk_by_col:
                fk = fk_by_col[col]
                attr = safe_identifier(col[:-2]) if col.endswith("ID") else safe_identifier(col)
                ref_class = safe_class_name(fk["ref_table"])

                nullable = sql.columns[col]["nullable"]
                args = [
                    f'"{ref_class}"',
                    f'db_column="{col}"',
                    "on_delete=models.DO_NOTHING",
                    'related_name="+"',
                ]
                if nullable:
                    args += ["null=True", "blank=True"]
                # primary key FK? rare but possible
                if len(sql.pk) == 1 and col == sql.pk[0]:
                    args.append("primary_key=True")

                out.append(f"    {attr} = models.ForeignKey({', '.join(args)})")
                continue

            # Determine field class from swagger if possible
            prop = api_props.get(col)
            field_cls, kwargs = swagger_type_to_django(prop) if prop else ("models.TextField", {})

            # Override with SQL constraints if SQL column exists
            if col in sql.columns:
                sql_type = sql.columns[col]["type"]
                nullable = sql.columns[col]["nullable"]

                override_cls, override_kwargs = sql_type_override(sql_type)
                if override_cls:
                    field_cls = override_cls
                # merge sql overrides (max_length, max_digits, decimal_places)
                kwargs.update(override_kwargs)

                # force null/blank from SQL nullability (authoritative)
                if nullable:
                    kwargs["null"] = True
                    kwargs["blank"] = True
                else:
                    kwargs.pop("null", None)
                    kwargs.pop("blank", None)

            # db_column
            kwargs["db_column"] = col

            # PK if applicable and SQL knows it
            if len(sql.pk) == 1 and col == sql.pk[0]:
                kwargs["primary_key"] = True

            # python field name
            fname = safe_identifier(col)

            # avoid reserved python keywords
            if is_reserved_identifier(fname):
                fname = f"{fname}_field"

            args = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
            out.append(f"    {fname} = {field_cls}({args})")

        # Meta
        out.append("")
        out.append("    class Meta:")
        out.append(f'        db_table = "autocare_{self.db}.{camel_to_snake(table)}"')
        out.append("        managed = True")

        # Composite PK
        if len(sql.pk) > 1:
            fields = [safe_identifier(c) for c in sql.pk]
            out.append("        constraints = [")
            out.append(
                f"            models.UniqueConstraint(fields={fields!r}, name='uniq_{camel_to_snake(table)}_pk'),"
            )
            out.append("        ]")

        return out

    def render_m2m(self) -> list[str]:
        """
        Add ManyToManyField for join tables.
        We do not create an explicit separate “promote_m2m” command anymore.
        """
        out: list[str] = []

        for table, sql in self.sql_tables.items():
            jt = infer_join_table(sql)
            if not jt:
                continue
            a, b = jt

            join_cls = safe_class_name(table)
            a_cls = safe_class_name(a)
            b_cls = safe_class_name(b)

            # Determine attribute names on each side
            # vehicles, bed_configs, etc. Keep predictable, collision-safe names.
            a_attr = safe_identifier(camel_to_snake(b)) + "s"
            b_attr = safe_identifier(camel_to_snake(a)) + "s"

            # Avoid ugly double-s and reserved words
            a_attr = a_attr.replace("classs", "classes")
            b_attr = b_attr.replace("classs", "classes")
            if is_reserved_identifier(a_attr):
                a_attr = a_attr + "_set"
            if is_reserved_identifier(b_attr):
                b_attr = b_attr + "_set"

            # Add fields using setattr at module import time.
            # This avoids editing class bodies and avoids import ordering.
            out.append(f"# {table} => M2M {a_cls} <-> {b_cls} through {join_cls}")
            out.append(
                f"setattr({a_cls}, {a_attr!r}, models.ManyToManyField("
                f"{b_cls!r}, through={join_cls!r}, related_name='+'))"
            )
            out.append(
                f"setattr({b_cls}, {b_attr!r}, models.ManyToManyField("
                f"{a_cls!r}, through={join_cls!r}, related_name='+'))"
            )
            out.append("")

        return out


# ----------------------------
# Command
# ----------------------------

class Command(BaseCommand):
    help = "Generate FINAL API-ingest Django models by merging SQL schema + OpenAPI swagger"

    def add_arguments(self, parser):
        parser.add_argument("--db", required=True, choices=["vcdb", "pcdb", "padb", "qdb"])
        parser.add_argument("--sql-schema", required=True)
        parser.add_argument("--openapi", required=True)
        parser.add_argument("--overwrite", action="store_true")

    def handle(self, *args, **opts):
        db = opts["db"]
        sql_path = Path(opts["sql_schema"]).resolve()
        openapi_path = Path(opts["openapi"]).resolve()

        # output target
        out_dir = Path(f"apps/autocare/models/{db}")
        if opts["overwrite"] and out_dir.exists():
            shutil.rmtree(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "__init__.py").touch(exist_ok=True)

        # Parse SQL schema
        raw_tables = parse_schema(sql_path)
        sql_tables: dict[str, SqlTable] = {}
        for tname, meta in raw_tables.items():
            sql_tables[tname] = SqlTable(
                name=tname,
                columns=meta["columns"],
                pk=meta.get("pk", []),
                fks=meta.get("fks", []),
            )

        # Parse OpenAPI
        api_models = load_openapi_models(openapi_path)

        writer = ModelWriter(db=db, sql_tables=sql_tables, api_models=api_models)
        code = writer.build()

        (out_dir / "models.py").write_text(code)
        self.stdout.write(self.style.SUCCESS(f"Final API models written: {out_dir / 'models.py'}"))
