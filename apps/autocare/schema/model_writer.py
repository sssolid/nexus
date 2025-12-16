from __future__ import annotations

from apps.autocare.schema.introspection import detect_base_class, is_m2m_table
from apps.autocare.schema.normalizer import safe_identifier, camel_to_snake, is_reserved_identifier


def sql_type_to_field(col_meta: dict) -> tuple[str, dict]:
    """
    Convert parsed column metadata into a Django field.
    col_meta = {"type": "VARCHAR(10)", "nullable": True}
    """
    sql_type = col_meta["type"]
    nullable = col_meta["nullable"]

    st = sql_type.strip().upper()
    kwargs: dict = {}

    if st.startswith("VARCHAR"):
        size = int(st.split("(")[1].rstrip(")"))
        field = "CharField"
        kwargs["max_length"] = size

    elif st in {"INT", "INTEGER"}:
        field = "IntegerField"

    elif st == "BIGINT":
        field = "BigIntegerField"

    elif st.startswith("DECIMAL") or st.startswith("NUMERIC"):
        field = "DecimalField"
        if "(" in st:
            inside = st.split("(")[1].rstrip(")")
            p, s = (int(x.strip()) for x in inside.split(","))
            kwargs["max_digits"] = p
            kwargs["decimal_places"] = s
        else:
            kwargs["max_digits"] = 10
            kwargs["decimal_places"] = 2

    elif st == "DATE":
        field = "DateField"

    elif "TIMESTAMP" in st or st == "DATETIME":
        field = "DateTimeField"

    elif st in {"BOOL", "BOOLEAN"}:
        field = "BooleanField"

    else:
        field = "TextField"

    if nullable:
        kwargs["null"] = True
        kwargs["blank"] = True

    return field, kwargs


def _kwargs_to_str(kwargs: dict) -> str:
    if not kwargs:
        return ""
    return ", ".join(f"{k}={v!r}" for k, v in kwargs.items())


def write_model(table: str, meta: dict, schema_name: str = "autocare_vcdb") -> str:
    """
    Generate a SCHEMA (mirror) model from SQL schema.
    """
    class_name = "".join(part.capitalize() for part in camel_to_snake(table).split("_"))
    if is_reserved_identifier(class_name.lower()):
        class_name += "Model"

    base_class = detect_base_class(meta["columns"])

    lines = [
        "from django.db import models",
    ]

    if base_class != "models.Model":
        lines.append("from apps.autocare.models.base import " + base_class)

    lines += [
        "",
        f"class {class_name}({base_class}):",
    ]

    pk_cols = meta.get("pk", [])

    for col, col_meta in meta["columns"].items():
        field_name = safe_identifier(col)

        field_cls, kwargs = sql_type_to_field(col_meta)

        # Always preserve db_column
        kwargs["db_column"] = col

        # Single-column PK
        if len(pk_cols) == 1 and col == pk_cols[0]:
            kwargs["primary_key"] = True

        lines.append(
            f"    {field_name} = models.{field_cls}({_kwargs_to_str(kwargs)})"
        )

    lines += [
        "",
        "    class Meta:",
        f'        db_table = "{schema_name}.{camel_to_snake(table)}"',
        "        managed = False",
    ]

    # Composite PK → UniqueConstraint
    if len(pk_cols) > 1:
        fields = [safe_identifier(c) for c in pk_cols]
        lines += [
            "        constraints = [",
            f"            models.UniqueConstraint(fields={fields!r}, name='uniq_{camel_to_snake(table)}_pk'),",
            "        ]",
        ]

    if is_m2m_table(meta):
        left = meta["fks"][0]["ref_table"]
        right = meta["fks"][1]["ref_table"]
        lines.append(f"    # M2M_JOIN_CANDIDATE: {left} <-> {right}")

    lines.append("")
    return "\n".join(lines)
