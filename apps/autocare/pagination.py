import json


def extract_pagination(response):
    """
    Extract pagination metadata from the X-Pagination header.
    Returns a dict or None.
    """
    header = response.headers.get("X-Pagination")
    return json.loads(header) if header else None
