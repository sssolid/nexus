TEMPORAL_FIELDS = {"culture_id", "effective_date", "end_date"}


def has_temporal_fields(field_names: set[str]) -> bool:
    return TEMPORAL_FIELDS.issubset(field_names)


def infer_name_field(field_names: set[str]) -> str | None:
    """
    Returns the *Name field if exactly one exists.
    """
    name_fields = [f for f in field_names if f.endswith("_name")]
    return name_fields[0] if len(name_fields) == 1 else None
