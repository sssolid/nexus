def infer_fk(field_name, fks):
    for fk in fks:
        if fk["column"] == field_name:
            return fk
    return None
