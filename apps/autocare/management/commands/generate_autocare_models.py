from __future__ import annotations

import ast
import json
import keyword
import re
import subprocess
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from django.core.management.base import BaseCommand
from django.db import connection


# ============================================================
# Paths / Config
# ============================================================

STAGING_SCHEMA_DEFAULT = "staging"
TARGET_SCHEMA_DEFAULT = "autocare_vcdb"

BASE_MODELS_DIR = Path("apps/autocare/models")
STAGING_RAW_FILE = BASE_MODELS_DIR / "staging_raw.py"

VCDB_DIR_DEFAULT = BASE_MODELS_DIR / "vcdb"
ARTIFACTS_DIR_DEFAULT = VCDB_DIR_DEFAULT / "_generated"

# Reserved/awkward model names
RESERVED_MODEL_NAMES = {
    "Class": "VehicleClass",
    "Model": "VehicleModel",
}

PYTHON_KEYWORDS = set(keyword.kwlist)


# ============================================================
# Naming helpers (authoritative)
# ============================================================

def safe_identifier(name: str) -> str:
    if not name:
        return "field"
    if name[0].isdigit():
        name = f"f_{name}"
    name = re.sub(r"[^0-9a-zA-Z_]+", "_", name)
    name = re.sub(r"__+", "_", name).strip("_") or "field"
    if name in PYTHON_KEYWORDS:
        name = name + "_"
    return name


def camel_to_snake(name: str) -> str:
    """
    Correctly handles acronym runs.

    Examples:
      VCdbChanges  -> vcdb_changes
      VCDBChanges  -> vcdb_changes
      DriveType    -> drive_type
      BedLengthID  -> bed_length_id
    """
    if not name:
        return name

    # Collapse acronym runs first: VCDBChanges -> VCDB_Changes
    s = re.sub(r"([A-Z]{2,})([A-Z][a-z])", r"\1_\2", name)

    # Split lower/digit before upper: DriveType -> Drive_Type
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s)

    return s.lower()


def table_to_class_name(table: str) -> str:
    """
    Prefer preserving existing CamelCase from quoted identifiers (e.g., DriveType).
    If underscore-separated, convert to CamelCase.
    If fully lowercase, TitleCase it.
    """
    if table in RESERVED_MODEL_NAMES:
        return RESERVED_MODEL_NAMES[table]

    if "_" in table:
        parts = [p for p in table.split("_") if p]
        return "".join(p[:1].upper() + p[1:] for p in parts)

    # If the table already contains internal capitals, keep them (but ensure leading capital)
    if any(c.isupper() for c in table[1:]):
        return table[:1].upper() + table[1:]

    return table[:1].upper() + table[1:]

def primary_key_attr_name(table_snake: str) -> str:
    return f"{table_snake}_id"

def normalize_model_class_name(raw: str) -> str:
    return RESERVED_MODEL_NAMES.get(raw, raw)


def snake_to_title(name: str) -> str:
    return name.replace("_", " ").strip().title()


def pluralize_simple(title: str) -> str:
    if title.endswith("s"):
        return title
    if title.endswith("y") and len(title) > 1 and title[-2].lower() not in "aeiou":
        return title[:-1] + "ies"
    return title + "s"


def ensure_trailing_id(snake: str) -> str:
    """
    For lowercase DB columns like 'attachmentid' or 'vehicleid',
    force them into 'attachment_id' or 'vehicle_id'.

    For already-correct 'bed_length_id', keep it.
    """
    if snake.endswith("_id"):
        return snake
    if snake.endswith("id") and len(snake) > 2:
        # attachmentid -> attachment_id
        return snake[:-2] + "_id"
    return snake


def fk_attr_from_db_column(db_col: str) -> str:
    """
    Convert a DB column name (any casing) to a ForeignKey attribute name WITHOUT '_id'.

    BedLengthID   -> bed_length
    attachmentid  -> attachment
    """
    snake = camel_to_snake(db_col)
    snake = ensure_trailing_id(snake)
    if snake.endswith("_id"):
        snake = snake[:-3]
    return safe_identifier(snake)


def non_fk_attr_from_db_column(db_col: str) -> str:
    """
    Convert a DB column name (any casing) to a normal field attribute name.

    BedLengthID  -> bed_length_id
    attachmentid -> attachment_id
    """
    snake = camel_to_snake(db_col)
    snake = ensure_trailing_id(snake)
    return safe_identifier(snake)


def parse_psql_index_columns(indexdef: str) -> Optional[List[str]]:
    """
    Parse simple btree indexes from pg_indexes.indexdef.
    Returns list of column names or None if expression / unsupported.
    """
    m = re.search(r"USING\s+btree\s*\((.+)\)", indexdef, re.IGNORECASE)
    if not m:
        return None
    inner = m.group(1).strip()

    # avoid expression/functional indexes
    if "(" in inner or ")" in inner:
        return None

    parts = [p.strip() for p in inner.split(",")]
    cols: List[str] = []
    for p in parts:
        p = re.sub(r"\s+(ASC|DESC)\b", "", p, flags=re.IGNORECASE).strip()
        p = re.sub(r"\s+NULLS\s+(FIRST|LAST)\b", "", p, flags=re.IGNORECASE).strip()

        if p.startswith('"') and p.endswith('"') and len(p) >= 2:
            p = p[1:-1]

        if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", p):
            return None
        cols.append(p)

    return cols or None


# ============================================================
# AST representations
# ============================================================

@dataclass
class FieldDef:
    original_attr: str
    field_type: str
    args: List[ast.AST]
    keywords: Dict[str, ast.AST]


@dataclass
class ModelDef:
    raw_class_name: str
    db_table: str
    fields: List[FieldDef]


# ============================================================
# Command
# ============================================================

class Command(BaseCommand):
    help = "Generate cleaned VCDB Django models from a staging schema (one file per model)."

    def add_arguments(self, parser):
        parser.add_argument("--staging-schema", default=STAGING_SCHEMA_DEFAULT)
        parser.add_argument("--target-schema", default=TARGET_SCHEMA_DEFAULT)
        parser.add_argument("--output-dir", default=str(VCDB_DIR_DEFAULT))
        parser.add_argument("--artifacts-dir", default=str(ARTIFACTS_DIR_DEFAULT))
        parser.add_argument("--overwrite", action="store_true", default=True)

    def handle(self, *args, **opts):
        staging_schema: str = opts["staging_schema"]
        target_schema: str = opts["target_schema"]
        output_dir = Path(opts["output_dir"])
        artifacts_dir = Path(opts["artifacts_dir"])
        overwrite: bool = bool(opts["overwrite"])

        output_dir.mkdir(parents=True, exist_ok=True)
        artifacts_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "__init__.py").touch()

        self.stdout.write("▶ Discovering staging tables")
        tables = self.get_tables(schema=staging_schema)

        self.stdout.write("▶ Generating staging_raw.py via inspectdb")
        self.generate_staging_raw(tables=tables)

        self.stdout.write("▶ Extracting DB metadata (PK/FK/indexes)")
        meta = self.extract_metadata(schema=staging_schema)
        self.write_artifacts(artifacts_dir, meta)

        self.stdout.write("▶ Parsing staging_raw.py")
        model_defs = self.parse_staging_raw()

        self.stdout.write("▶ Generating cleaned model files")
        self.generate_model_files(
            model_defs=model_defs,
            metadata=meta,
            output_dir=output_dir,
            target_schema=target_schema,
            overwrite=overwrite,
        )

        self.stdout.write(self.style.SUCCESS("✔ Autocare VCDB model generation complete"))

    # ---------------------------
    # DB metadata / tables
    # ---------------------------

    def get_tables(self, schema: str) -> List[str]:
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

    def extract_metadata(self, schema: str) -> Dict[str, Any]:
        primary_keys: Dict[str, List[str]] = defaultdict(list)
        foreign_keys: Dict[str, List[Dict[str, str]]] = defaultdict(list)
        indexes: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

        with connection.cursor() as cur:
            # PKs
            cur.execute(
                """
                SELECT tc.table_name, kcu.column_name, kcu.ordinal_position
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu
                  ON tc.constraint_name = kcu.constraint_name
                 AND tc.table_schema = kcu.table_schema
                WHERE tc.constraint_type = 'PRIMARY KEY'
                  AND tc.table_schema = %s
                ORDER BY tc.table_name, kcu.ordinal_position;
                """,
                [schema],
            )
            for table, col, _pos in cur.fetchall():
                primary_keys[table].append(col)

            # FKs
            cur.execute(
                """
                SELECT
                  tc.table_name,
                  kcu.column_name,
                  ccu.table_name AS foreign_table_name,
                  ccu.column_name AS foreign_column_name,
                  tc.constraint_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu
                  ON tc.constraint_name = kcu.constraint_name
                 AND tc.table_schema = kcu.table_schema
                JOIN information_schema.constraint_column_usage ccu
                  ON ccu.constraint_name = tc.constraint_name
                 AND ccu.table_schema = tc.table_schema
                WHERE tc.constraint_type = 'FOREIGN KEY'
                  AND tc.table_schema = %s
                ORDER BY tc.table_name, kcu.ordinal_position;
                """,
                [schema],
            )
            for table, col, ft, fc, cname in cur.fetchall():
                foreign_keys[table].append(
                    {
                        "column": col,
                        "ref_table": ft,
                        "ref_column": fc,
                        "constraint": cname,
                    }
                )

            # Indexes
            cur.execute(
                """
                SELECT tablename, indexdef
                FROM pg_indexes
                WHERE schemaname = %s
                ORDER BY tablename, indexname;
                """,
                [schema],
            )
            for table, indexdef in cur.fetchall():
                cols = parse_psql_index_columns(indexdef)
                indexes[table].append({"indexdef": indexdef, "columns": cols})

        return {
            "schema": schema,
            "primary_keys": dict(primary_keys),
            "foreign_keys": dict(foreign_keys),
            "indexes": dict(indexes),
        }

    def write_artifacts(self, artifacts_dir: Path, meta: Dict[str, Any]) -> None:
        (artifacts_dir / "primary_keys.json").write_text(json.dumps(meta["primary_keys"], indent=2, sort_keys=True) + "\n")
        (artifacts_dir / "foreign_keys.json").write_text(json.dumps(meta["foreign_keys"], indent=2, sort_keys=True) + "\n")
        (artifacts_dir / "indexes.json").write_text(json.dumps(meta["indexes"], indent=2, sort_keys=True) + "\n")

    # ---------------------------
    # inspectdb
    # ---------------------------

    def generate_staging_raw(self, tables: List[str]) -> None:
        cmd = ["python", "manage.py", "inspectdb", *tables]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        STAGING_RAW_FILE.write_text(result.stdout, encoding="utf-8")

    # ---------------------------
    # parse staging_raw
    # ---------------------------

    def parse_staging_raw(self) -> List[ModelDef]:
        src = STAGING_RAW_FILE.read_text(encoding="utf-8")
        tree = ast.parse(src)

        models: List[ModelDef] = []

        for node in tree.body:
            if not isinstance(node, ast.ClassDef):
                continue

            raw_class_name = node.name
            fields: List[FieldDef] = []
            db_table = raw_class_name  # fallback if not present

            for item in node.body:
                if isinstance(item, ast.Assign) and len(item.targets) == 1 and isinstance(item.targets[0], ast.Name):
                    target = item.targets[0].id
                    call = item.value
                    if not isinstance(call, ast.Call):
                        continue
                    if not isinstance(call.func, ast.Attribute):
                        continue

                    field_type = call.func.attr
                    keywords = {kw.arg: kw.value for kw in call.keywords if kw.arg}
                    fields.append(FieldDef(original_attr=target, field_type=field_type, args=list(call.args), keywords=keywords))

                if isinstance(item, ast.ClassDef) and item.name == "Meta":
                    for meta_stmt in item.body:
                        if isinstance(meta_stmt, ast.Assign) and len(meta_stmt.targets) == 1 and isinstance(meta_stmt.targets[0], ast.Name):
                            k = meta_stmt.targets[0].id
                            v = meta_stmt.value
                            if k == "db_table" and isinstance(v, ast.Constant) and isinstance(v.value, str):
                                db_table = v.value

            models.append(ModelDef(raw_class_name=raw_class_name, db_table=db_table, fields=fields))

        return models

    # ---------------------------
    # generate files
    # ---------------------------

    def generate_model_files(
        self,
        model_defs: List[ModelDef],
        metadata: Dict[str, Any],
        output_dir: Path,
        target_schema: str,
        overwrite: bool,
    ) -> None:
        pk_map: Dict[str, List[str]] = metadata.get("primary_keys", {})
        fk_map: Dict[str, List[Dict[str, str]]] = metadata.get("foreign_keys", {})
        idx_map: Dict[str, List[Dict[str, Any]]] = metadata.get("indexes", {})

        init_imports: List[str] = []

        for m in model_defs:
            source_table = m.db_table  # table name as returned by inspectdb (no schema prefix)
            table_snake = camel_to_snake(source_table)
            module_name = safe_identifier(table_snake)

            file_path = output_dir / f"{module_name}.py"
            if file_path.exists() and not overwrite:
                continue

            class_name = table_to_class_name(source_table)
            verbose_name = snake_to_title(table_snake)
            verbose_name_plural = pluralize_simple(verbose_name)

            pk_cols = pk_map.get(source_table, [])
            composite_pk = len(pk_cols) > 1

            # map db_column -> FK metadata
            fk_by_col = {fk["column"]: fk for fk in fk_map.get(source_table, [])}

            # Build mapping of DB column -> python attr (non-FK) for index resolution
            col_to_attr: Dict[str, str] = {}
            for f in m.fields:
                db_col = self.get_db_column(f)
                if db_col:
                    col_to_attr[db_col] = non_fk_attr_from_db_column(db_col)

            lines: List[str] = []
            lines.append("from django.db import models")
            lines.append("from apps.autocare.models.mixins import AutocareAPIMetadata")
            lines.append("")
            lines.append("")
            lines.append(f"class {class_name}(AutocareAPIMetadata, models.Model):")

            # If a table is truly empty (shouldn't happen), keep class valid
            wrote_any = False

            for f in m.fields:
                db_col = self.get_db_column(f)
                if not db_col:
                    continue

                field_type = f.field_type
                wrote_any = True

                # Start with kwargs from inspectdb, but normalize key things
                kwargs_code: Dict[str, str] = {}
                for k, v_node in f.keywords.items():
                    if k == "on_delete":
                        kwargs_code["on_delete"] = "models.DO_NOTHING"
                        continue
                    if k == "db_column":
                        # overwrite with the value we computed as db_col
                        kwargs_code["db_column"] = repr(db_col)
                        continue
                    if isinstance(v_node, ast.Constant):
                        kwargs_code[k] = repr(v_node.value)
                    else:
                        kwargs_code[k] = ast.unparse(v_node)

                # Always include db_column, even when inspectdb omitted it
                kwargs_code["db_column"] = repr(db_col)

                if db_col in pk_cols:
                    kwargs_code["primary_key"] = "True"

                if field_type == "ForeignKey":
                    fk_meta = fk_by_col.get(db_col)
                    ref_table = fk_meta["ref_table"] if fk_meta else ""
                    target_class = table_to_class_name(ref_table) if ref_table else "UNKNOWN"

                    # Self-referential FK handling
                    if ref_table == source_table:
                        attr = f"parent_{camel_to_snake(source_table)}"
                        related_name = "children"
                    else:
                        attr = safe_identifier(camel_to_snake(target_class))
                        related_name = None

                    kwargs_code["db_index"] = "True"
                    kwargs_code["on_delete"] = "models.DO_NOTHING"

                    if related_name:
                        kwargs_code["related_name"] = repr(related_name)

                    rendered = self.render_field_line(
                        attr=attr,
                        field_type="ForeignKey",
                        positional=[repr(target_class)],
                        kwargs=kwargs_code,
                    )
                    lines.append(f"    {rendered}")
                else:
                    # Non-FK fields
                    # NEVER allow a model attribute named "id" (Django reserves it)
                    if db_col.upper() == "ID":
                        attr = primary_key_attr_name(table_snake)
                    else:
                        attr = non_fk_attr_from_db_column(db_col)

                    rendered = self.render_field_line(
                        attr=attr,
                        field_type=field_type,
                        positional=[],
                        kwargs=kwargs_code,
                    )
                    lines.append(f"    {rendered}")

            if not wrote_any:
                lines.append("    pass")

            # __str__
            lines.append("")
            lines.append("    def __str__(self) -> str:")
            lines.append("        return f\"{self.__class__.__name__}({self.pk})\"")

            # Meta
            lines.append("")
            lines.append("    class Meta:")
            lines.append("        managed = True")
            schema_qualified = f'"{target_schema}"."{table_snake}"'
            lines.append(f"        db_table = {repr(schema_qualified)}")
            lines.append(f"        verbose_name = {repr(verbose_name)}")
            lines.append(f"        verbose_name_plural = {repr(verbose_name_plural)}")

            if composite_pk:
                lines.append("        # WARNING: composite primary key detected in DB; Django cannot enforce it natively.")
                lines.append(f"        # DB PK columns: {pk_cols!r}")

            index_lines = self.generate_meta_indexes(
                table=source_table,
                idx_map=idx_map,
                col_to_attr=col_to_attr,
            )
            if index_lines:
                lines.append("        indexes = [")
                for ln in index_lines:
                    lines.append(f"            {ln}")
                lines.append("        ]")

            lines.append("")

            file_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            init_imports.append(f"from .{module_name} import {class_name}")

        (output_dir / "__init__.py").write_text("\n".join(sorted(set(init_imports))) + "\n", encoding="utf-8")

    # ---------------------------
    # Core helpers (fixed)
    # ---------------------------

    def get_db_column(self, f: FieldDef) -> Optional[str]:
        """
        If inspectdb included db_column, use it.
        If it did NOT, then the attribute name IS the db column name.
        This is the key fix for your lowercase attachment tables.
        """
        v = f.keywords.get("db_column")
        if isinstance(v, ast.Constant) and isinstance(v.value, str):
            return v.value
        return f.original_attr  # fallback

    def generate_meta_indexes(
        self,
        table: str,
        idx_map: Dict[str, List[Dict[str, Any]]],
        col_to_attr: Dict[str, str],
    ) -> List[str]:
        """
        Convert DB index columns -> MODEL FIELD NAMES.

        Important:
        - FK fields are generated as <name> (no _id), so an index on BedLengthID
          should point to bed_length, not bed_length_id.
        - Lowercase cols like attachmentid become attachment_id.
        """
        out: List[str] = []
        for idx in idx_map.get(table, []):
            cols = idx.get("columns")
            if not cols or len(cols) != 1:
                continue

            col = cols[0]

            # First: if we already mapped it (non-FK default)
            attr = col_to_attr.get(col)

            # Next: if the column ends with id, it might be FK -> generate FK attr
            if not attr and col.lower().endswith("id"):
                attr = fk_attr_from_db_column(col)

            # Final fallback: non-FK naming
            if not attr:
                attr = non_fk_attr_from_db_column(col)

            if attr:
                out.append(f"models.Index(fields={[attr]!r})")

        return out

    def render_field_line(self, attr: str, field_type: str, positional: List[str], kwargs: Dict[str, str]) -> str:
        """
        Deterministic kwargs ordering (db_column, primary_key early).
        """
        ordered_keys = list(kwargs.keys())
        if "db_column" in ordered_keys:
            ordered_keys.remove("db_column")
            ordered_keys.insert(0, "db_column")
        if "primary_key" in ordered_keys:
            ordered_keys.remove("primary_key")
            insert_at = 1 if "db_column" in ordered_keys else 0
            ordered_keys.insert(insert_at, "primary_key")

        parts: List[str] = []
        parts.extend(positional)
        parts.extend([f"{k}={kwargs[k]}" for k in ordered_keys])

        return f"{safe_identifier(attr)} = models.{field_type}({', '.join(parts)})"
