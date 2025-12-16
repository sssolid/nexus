def detect_base_class(columns: dict) -> str:
    colset = set(columns.keys())

    temporal = {
        "CultureID",
        "EffectiveDateTime",
        "EndDateTime",
    }

    if not temporal.issubset(colset):
        return "models.Model"

    name_cols = [c for c in colset if c.endswith("Name")]

    if len(name_cols) == 1:
        return "AutocareNamedModel"

    return "AutocareTemporalModel"

def is_m2m_table(meta: dict) -> bool:
    fks = meta.get("fks", [])
    columns = meta.get("columns", {}).keys()

    if len(fks) != 2:
        return False

    # Only allow simple join metadata
    allowed_extras = {"Source", "CultureID", "EffectiveDateTime", "EndDateTime"}
    fk_cols = {fk["column"] for fk in fks}

    for col in columns:
        if col not in fk_cols and col not in allowed_extras:
            return False

    return True

