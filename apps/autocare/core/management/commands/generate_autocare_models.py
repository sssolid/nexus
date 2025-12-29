from __future__ import annotations

import keyword
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple, Any, Set

from django.core.management.base import BaseCommand, CommandError
from django.db import connection

PYTHON_KEYWORDS = set(keyword.kwlist)

TYPE_MAP = {
    "integer": "IntegerField",
    "bigint": "BigIntegerField",
    "smallint": "SmallIntegerField",
    "character varying": "CharField",
    "varchar": "CharField",
    "text": "TextField",
    "boolean": "BooleanField",
    "date": "DateField",
    "timestamp without time zone": "DateTimeField",
    "timestamp with time zone": "DateTimeField",
    "double precision": "FloatField",
    "numeric": "DecimalField",
    "real": "FloatField",
}


def safe_identifier(name: str) -> str:
    if not name:
        return "field"
    name = re.sub(r"[^0-9a-zA-Z_]", "_", name)
    name = re.sub(r"__+", "_", name).strip("_") or "field"
    if name[0].isdigit():
        name = f"f_{name}"
    if name in PYTHON_KEYWORDS:
        name = name + "_"
    return name


def camel_to_snake(name: str) -> str:
    # Handles acronym runs: MetaUOMID -> meta_uom_id, VCDBChanges -> vcdb_changes
    s = re.sub(r"([A-Z]{2,})([A-Z][a-z])", r"\1_\2", name)
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s)
    return s.lower()


def table_to_class_name(table: str) -> str:
    """
    Preserve CamelCase tables (MeasurementGroup, MetaUOMCodes).
    Convert underscore_names to CamelCase.
    """
    if "_" in table:
        parts = [p for p in table.split("_") if p]
        return "".join(p[:1].upper() + p[1:] for p in parts)

    # If internal capitals exist, keep them.
    if any(c.isupper() for c in table[1:]):
        return table[:1].upper() + table[1:]

    # Fallback: title-case first letter only
    return table[:1].upper() + table[1:]


def fk_attr_from_db_column(db_col: str) -> str:
    """
    MeasurementGroupID -> measurement_group
    VehicleTypeID      -> vehicle_type
    """
    snake = camel_to_snake(db_col)
    if snake.endswith("_id"):
        snake = snake[:-3]
    return safe_identifier(snake)


def non_fk_attr_from_db_column(db_col: str) -> str:
    """
    MeasurementGroupID -> measurement_group_id (for non-FK int fields)
    """
    return safe_identifier(camel_to_snake(db_col))


def parse_pg_index_columns(indexdef: str) -> List[str] | None:
    """
    Parse basic btree index column list out of pg_indexes.indexdef.

    Returns a list of column names (as stored in the DB) or None for unsupported indexes.
    """
    m = re.search(r"USING\s+btree\s*\((.+)\)", indexdef, re.IGNORECASE)
    if not m:
        return None
    inner = m.group(1).strip()

    # Skip functional/expression indexes
    if "(" in inner or ")" in inner:
        return None

    parts = [p.strip() for p in inner.split(",")]
    cols: List[str] = []
    for p in parts:
        p = re.sub(r"\s+(ASC|DESC)\b", "", p, flags=re.IGNORECASE).strip()
        p = re.sub(r"\s+NULLS\s+(FIRST|LAST)\b", "", p, flags=re.IGNORECASE).strip()
        if p.startswith('"') and p.endswith('"') and len(p) >= 2:
            p = p[1:-1]
        # Only allow simple identifiers
        if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", p):
            return None
        cols.append(p)
    return cols or None


def infer_app_label_from_output_dir(output_dir: Path) -> str:
    name = output_dir.name.lower()
    if name in {"vcdb", "pcdb", "padb", "qdb"}:
        return f"autocare_{name}"
    return "autocare"


class Command(BaseCommand):
    help = "Generate Django models (PK/FK/index) from a Postgres schema without inspectdb."

    def add_arguments(self, parser):
        parser.add_argument("--schema", required=True)
        parser.add_argument("--output-dir", required=True)
        parser.add_argument("--target-schema", default=None)
        parser.add_argument("--managed", action="store_true", default=True)

    def handle(self, *args, **opts):
        schema: str = opts["schema"]
        output_dir = Path(opts["output_dir"])
        app_label = infer_app_label_from_output_dir(output_dir)
        target_schema: str | None = opts["target_schema"]
        managed: bool = bool(opts["managed"])

        # If not provided, default: staging_x -> autocare_x, otherwise same as schema
        if target_schema is None:
            target_schema = schema.replace("staging_", "autocare_") if schema.startswith("staging_") else schema

        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "__init__.py").touch()

        tables = self.get_tables(schema)
        if not tables:
            raise CommandError(f"No tables found in schema '{schema}'")

        columns = self.get_columns(schema)
        primary_keys = self.get_primary_keys(schema)
        foreign_keys = self.get_foreign_keys(schema)
        indexes = self.get_indexes(schema)

        import_lines: Set[str] = set()

        for table in tables:
            self.write_model(
                schema=schema,
                target_schema=target_schema,
                table=table,
                cols=columns.get(table, []),
                pk_cols=set(primary_keys.get(table, [])),
                fk_map=foreign_keys.get(table, {}),
                index_cols=indexes.get(table, []),
                outdir=output_dir,
                managed=managed,
                app_label=app_label,
            )
            class_name = table_to_class_name(table)
            module_name = safe_identifier(camel_to_snake(table))
            import_lines.add(f"from .{module_name} import {class_name}")

        init_file = output_dir / "__init__.py"
        init_file.write_text("\n".join(sorted(import_lines)) + "\n", encoding="utf-8")

        self.stdout.write(self.style.SUCCESS(f"✔ Generated models for {schema} → {target_schema} in {output_dir}"))

    # -------------------------
    # Introspection
    # -------------------------

    def get_tables(self, schema: str) -> List[str]:
        with connection.cursor() as cur:
            cur.execute(
                """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = %s
                  AND table_type = 'BASE TABLE'
                ORDER BY table_name;
                """,
                [schema],
            )
            return [r[0] for r in cur.fetchall()]

    def get_columns(self, schema: str) -> Dict[str, List[Dict[str, Any]]]:
        out: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        with connection.cursor() as cur:
            cur.execute(
                """
                SELECT
                    table_name,
                    column_name,
                    data_type,
                    is_nullable,
                    character_maximum_length,
                    numeric_precision,
                    numeric_scale
                FROM information_schema.columns
                WHERE table_schema = %s
                ORDER BY table_name, ordinal_position;
                """,
                [schema],
            )
            for (
                table,
                col,
                dt,
                nullable,
                char_len,
                precision,
                scale,
            ) in cur.fetchall():
                out[table].append(
                    {
                        "name": col,
                        "type": dt,
                        "nullable": (nullable == "YES"),
                        "maxlen": char_len,
                        "precision": precision,
                        "scale": scale,
                    }
                )
        return out

    def get_primary_keys(self, schema: str) -> Dict[str, List[str]]:
        out: Dict[str, List[str]] = defaultdict(list)
        with connection.cursor() as cur:
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
                out[table].append(col)
        return out

    def get_foreign_keys(self, schema: str) -> Dict[str, Dict[str, Tuple[str, str]]]:
        """
        Returns {table: {column: (ref_table, ref_column)}}
        """
        out: Dict[str, Dict[str, Tuple[str, str]]] = defaultdict(dict)
        with connection.cursor() as cur:
            cur.execute(
                """
                SELECT
                  tc.table_name,
                  kcu.column_name,
                  ccu.table_name AS foreign_table_name,
                  ccu.column_name AS foreign_column_name
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
            for table, col, ref_table, ref_col in cur.fetchall():
                out[table][col] = (ref_table, ref_col)
        return out

    def get_indexes(self, schema: str) -> Dict[str, List[List[str]]]:
        """
        Returns {table: [ [col1], [col2], [colA, colB], ... ]} for simple btree indexes.
        """
        out: Dict[str, List[List[str]]] = defaultdict(list)
        with connection.cursor() as cur:
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
                cols = parse_pg_index_columns(indexdef)
                if cols:
                    out[table].append(cols)
        return out

    # -------------------------
    # Code generation
    # -------------------------

    def write_model(
        self,
        schema: str,
        target_schema: str,
        table: str,
        cols: List[Dict[str, Any]],
        pk_cols: set[str],
        fk_map: Dict[str, Tuple[str, str]],
        index_cols: List[List[str]],
        outdir: Path,
        managed: bool,
        app_label: str,
    ) -> None:
        class_name = table_to_class_name(table)
        module_name = safe_identifier(camel_to_snake(table))
        file_path = outdir / f"{module_name}.py"

        lines: List[str] = [
            "from django.db import models",
            "from apps.autocare.core.mixins import AutocareAPIMetadata",
            "",
            "",
            f"class {class_name}(AutocareAPIMetadata, models.Model):",
        ]

        wrote_any = False

        # Map db_column -> python attr for index resolution
        # (FK columns map to FK attr without _id)
        col_to_attr: Dict[str, str] = {}

        for c in cols:
            db_col = c["name"]
            wrote_any = True

            if db_col in fk_map:
                # FK field
                attr = fk_attr_from_db_column(db_col)
                ref_table, _ref_col = fk_map[db_col]
                ref_cls = table_to_class_name(ref_table)
                ref_app_label = app_label

                lines.append(
                    f"    {attr} = models.ForeignKey("
                    f"'{ref_app_label}.{ref_cls}', db_column='{db_col}', db_index=True, on_delete=models.DO_NOTHING)"
                )
                col_to_attr[db_col] = attr
                continue

            # Normal field
            attr = non_fk_attr_from_db_column(db_col)
            field_type = TYPE_MAP.get(c["type"], "TextField")

            kwargs: List[str] = [f"db_column='{db_col}'"]

            if field_type == "CharField" and c.get("maxlen"):
                kwargs.append(f"max_length={int(c['maxlen'])}")

            if field_type == "DecimalField":
                # best-effort defaults
                prec = c.get("precision") or 18
                scale = c.get("scale") or 6
                kwargs.append(f"max_digits={int(prec)}")
                kwargs.append(f"decimal_places={int(scale)}")

            if db_col in pk_cols:
                kwargs.append("primary_key=True")

            if c.get("nullable"):
                kwargs.append("null=True")
                kwargs.append("blank=True")

            lines.append(f"    {attr} = models.{field_type}({', '.join(kwargs)})")
            col_to_attr[db_col] = attr

        if not wrote_any:
            lines.append("    pass")

        lines += [
            "",
            "    def __str__(self) -> str:",
            '        return f"{self.__class__.__name__}({self.pk})"',
            "",
            "    class Meta:",
            f"        app_label = '{app_label}'",
            f"        managed = {bool(managed)}",
            f"        db_table = '\"{target_schema}\".\"{table}\"'",
            f"        verbose_name = '{class_name}'",
            f"        verbose_name_plural = '{class_name}s'",
        ]

        # Indexes: convert db column names to model field names
        idx_lines: List[str] = []
        for cols_list in index_cols:
            # map each column to model attr if known, else fall back to snake-case
            fields: List[str] = []
            ok = True
            for db_col in cols_list:
                attr = col_to_attr.get(db_col)
                if not attr:
                    # fallback: treat as non-fk
                    attr = non_fk_attr_from_db_column(db_col)
                if not attr:
                    ok = False
                    break
                fields.append(attr)
            if ok and fields:
                idx_lines.append(f"            models.Index(fields={fields!r}),")

        if idx_lines:
            lines.append("        indexes = [")
            lines.extend(idx_lines)
            lines.append("        ]")
        else:
            lines.append("        indexes = []")

        lines.append("")
        file_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
