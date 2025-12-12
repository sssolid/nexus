import re
from apps.data_sync.models import DataMapping

def apply_mapping(filemaker_row, target_model):
    mappings = DataMapping.objects.filter(
        target_model=target_model,
        is_active=True,
    )

    output = {}

    for m in mappings:
        raw_value = filemaker_row.get(m.filemaker_field)

        if raw_value is None and m.is_required:
            raise ValueError(f"Missing required field: {m.filemaker_field}")

        # Apply default value
        if raw_value is None and m.default_value:
            raw_value = m.default_value

        # Apply transformation function if exists
        if m.transformation_function:
            fn = resolve_function(m.transformation_function)
            raw_value = fn(raw_value)

        # Apply regex validation
        if m.validation_regex:
            if raw_value and not re.match(m.validation_regex, str(raw_value)):
                raise ValueError(f"Validation failed for {m.target_field}")

        output[m.target_field] = raw_value

    return output


def resolve_function(fn_path):
    """
    Accepts:  'module.function'  or inline Python  'lambda x: x.strip()'
    """
    if fn_path.strip().startswith("lambda"):
        return eval(fn_path)

    module_name, fn_name = fn_path.rsplit(".", 1)
    module = __import__(module_name, fromlist=[fn_name])
    return getattr(module, fn_name)
