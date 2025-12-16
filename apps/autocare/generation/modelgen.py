import re
from dataclasses import dataclass
from typing import Dict, Any, Optional

COMMON_TEMPORAL = {"CultureID", "EffectiveDateTime", "EndDateTime"}


def infer_field_expr(sw_type: str, sw_format: Optional[str], nullable: bool, db_index: bool) -> str:
    args = []
    if nullable:
        args.append("null=True")
        args.append("blank=True")
    if db_index:
        args.append("db_index=True")

    kw = ""
    if args:
        kw = ", " + ", ".join(args)

    if sw_type == "integer":
        return f"models.IntegerField({kw.lstrip(', ')})" if kw else "models.IntegerField()"
    if sw_type == "number":
        return f"models.FloatField({kw.lstrip(', ')})" if kw else "models.FloatField()"
    if sw_type == "boolean":
        return f"models.BooleanField({kw.lstrip(', ')})" if kw else "models.BooleanField()"
    if sw_type == "string" and sw_format == "date-time":
        return f"models.DateTimeField({kw.lstrip(', ')})" if kw else "models.DateTimeField()"

    # Default string
    return f"models.CharField(max_length=255{kw})"


def guess_base_class(model_name: str, swagger_props: Dict[str, Any]) -> str:
    keys = set(swagger_props.keys())
    if COMMON_TEMPORAL.issubset(keys):
        # check name-like property
        name_key = f"{model_name}Name"
        if name_key in keys:
            return "AutocareNamedModel"
        return "AutocareTemporalModel"
    return "models.Model"


def guess_pk_field(model_name: str, swagger_props: Dict[str, Any]) -> Optional[str]:
    """
    Prefer ModelNameID if present (MakeID, ModelID, YearID, etc.).
    Avoid guessing PK for join tables.
    """
    candidate = f"{model_name}ID"
    if candidate in swagger_props:
        return candidate

    # If there's exactly one *ID field and it ends with ID, we *could* pick it,
    # but join tables will usually have 2+ IDs. So only do this when exactly 1.
    id_fields = [k for k in swagger_props.keys() if k.endswith("ID")]
    if len(id_fields) == 1:
        return id_fields[0]

    return None


def guess_name_key(model_name: str, swagger_props: Dict[str, Any]) -> Optional[str]:
    """
    The common case: {ModelName}Name.
    Some tables use a different label (e.g. BedLength has BedLength).
    This returns the best guess for 'name' semantics.
    """
    if f"{model_name}Name" in swagger_props:
        return f"{model_name}Name"
    # fallback: a single string field that is not CultureID and not a datetime
    string_fields = []
    for k, v in swagger_props.items():
        if k in COMMON_TEMPORAL:
            continue
        if v.get("type") == "string" and v.get("format") not in ("date-time", "date"):
            string_fields.append(k)
    if len(string_fields) == 1:
        return string_fields[0]
    return None


@dataclass
class GeneratedModel:
    model_name: str
    base_class: str
    pk_key: Optional[str]
    name_key: Optional[str]
    fields: Dict[str, str]  # snake_name -> field_expr
