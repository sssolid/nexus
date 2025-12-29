from __future__ import annotations

import keyword
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

from django.core.management.base import BaseCommand, CommandError
from django.db import connection

BASE_OUT = Path("apps/autocare/models/_staging_dump")

PYTHON_KEYWORDS = set(keyword.kwlist)

SQL_TO_DJANGO = {
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


def safe(name: str) -> str:
    name = re.sub(r"[^0-9a-zA-Z_]", "_", name)
    if name[0].isdigit():
        name = f"f_{name}"
    if name in PYTHON_KEYWORDS:
        name += "_"
    return name.lower()


class Command(BaseCommand):
    help = "Generate Django models with PK/FK support from a PostgreSQL staging schema."

    def add_arguments(self, parser):
        parser.add_argument("--schema", required=True)
        parser.add_argument("--output-dir", required=True)

    def handle(self, *args, **opts):
        schema = opts["schema"]
        outdir = BASE_OUT / opts["output_dir"]
        outdir.mkdir(parents=True, exist_ok=True)
        (outdir / "__init__.py").touch()

        tables = self.get_tables(schema)
        if not tables:
            raise CommandError(f"No tables found in schema '{schema}'")

        columns = self.get_columns(schema)
        fks = self.get_foreign_keys(schema)
        pks = self.get_primary_keys(schema)

        for table in tables:
            self.write_model(schema, table, columns[table], fks[table], pks[table], outdir)

        self.stdout.write(self.style.SUCCESS("Models generated successfully."))

    def get_tables(self, schema: str) -> List[str]:
        with connection.cursor() as cur:
            cur.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = %s
                ORDER BY table_name
            """, [schema])
            return [r[0] for r in cur.fetchall()]

    def get_columns(self, schema: str):
        out = defaultdict(list)
        with connection.cursor() as cur:
            cur.execute("""
                SELECT table_name, column_name, data_type,
                       is_nullable, character_maximum_length
                FROM information_schema.columns
                WHERE table_schema = %s
                ORDER BY table_name, ordinal_position
            """, [schema])
            for t, c, dt, nullable, maxlen in cur.fetchall():
                out[t].append({
                    "name": c,
                    "type": dt,
                    "nullable": nullable == "YES",
                    "maxlen": maxlen,
                })
        return out

    def get_primary_keys(self, schema: str):
        out = defaultdict(list)
        with connection.cursor() as cur:
            cur.execute("""
                SELECT tc.table_name, kcu.column_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu
                  ON tc.constraint_name = kcu.constraint_name
                 AND tc.table_schema = kcu.table_schema
                WHERE tc.constraint_type = 'PRIMARY KEY'
                  AND tc.table_schema = %s
            """, [schema])
            for t, c in cur.fetchall():
                out[t].append(c)
        return out

    def get_foreign_keys(self, schema: str):
        out = defaultdict(list)
        with connection.cursor() as cur:
            cur.execute("""
                SELECT
                    tc.table_name,
                    kcu.column_name,
                    ccu.table_name,
                    ccu.column_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu
                  ON tc.constraint_name = kcu.constraint_name
                 AND tc.table_schema = kcu.table_schema
                JOIN information_schema.constraint_column_usage ccu
                  ON ccu.constraint_name = tc.constraint_name
                 AND ccu.table_schema = tc.table_schema
                WHERE tc.constraint_type = 'FOREIGN KEY'
                  AND tc.table_schema = %s
            """, [schema])
            for t, col, rt, rc in cur.fetchall():
                out[t].append({"col": col, "ref_table": rt, "ref_col": rc})
        return out

    def write_model(self, schema, table, cols, fks, pks, outdir):
        class_name = "".join(p.capitalize() for p in table.split("_"))
        path = outdir / f"{table}.py"

        fk_cols = {fk["col"]: fk for fk in fks}

        lines = [
            "from django.db import models",
            "",
            f"class {class_name}(models.Model):"
        ]

        for col in cols:
            name = safe(col["name"])
            if col["name"] in fk_cols:
                fk = fk_cols[col["name"]]
                ref_class = "".join(p.capitalize() for p in fk["ref_table"].split("_"))
                lines.append(f"    {name} = models.ForeignKey('{ref_class}', db_column='{col['name']}', on_delete=models.DO_NOTHING)")
                continue

            ftype = SQL_TO_DJANGO.get(col["type"], "TextField")
            args = []
            if ftype == "CharField" and col["maxlen"]:
                args.append(f"max_length={col['maxlen']}")
            if col["name"] in pks[table]:
                args.append("primary_key=True")
            if col["nullable"]:
                args += ["null=True", "blank=True"]

            lines.append(f"    {name} = models.{ftype}({', '.join(args)})")

        lines += [
            "",
            "    class Meta:",
            "        managed = False",
            f"        db_table = '\"{schema}\".\"{table}\"'",
            "",
        ]

        path.write_text("\n".join(lines))
