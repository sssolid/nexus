def get_record_count(data):
    """
    Safely determine record count from Autocare API payloads.

    Handles:
    - List payloads
    - Common Swagger wrapper objects
    """
    if isinstance(data, list):
        return len(data)

    if isinstance(data, dict):
        for key in ("data", "items", "results"):
            value = data.get(key)
            if isinstance(value, list):
                return len(value)

    return None
