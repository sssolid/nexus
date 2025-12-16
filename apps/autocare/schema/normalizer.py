from __future__ import annotations

import keyword
import re

# Treat these as atomic tokens so MakeID -> make_id (not make_i_d)
ACRONYMS = {"ID", "VIN", "API", "OEM", "URL", "SKU"}

# Python keywords + a few Django/potential attribute collisions
_RESERVED = set(keyword.kwlist) | {
    "type",
    "id",          # avoid shadowing implicit ids in some contexts
    "class",
    "from",
    "import",
    "pass",
    "raise",
    "global",
    "nonlocal",
    "lambda",
    "with",
    "yield",
    "async",
    "await",
    "order",
}


def is_reserved_identifier(name: str) -> bool:
    return name in _RESERVED or keyword.iskeyword(name)


_TOKEN_RE = re.compile(r"[A-Z]+(?=[A-Z][a-z]|$)|[A-Z]?[a-z]+|\d+")


def camel_to_snake(name: str) -> str:
    """
    Acronym-aware CamelCase -> snake_case.

    Examples:
      MakeID -> make_id
      VehicleToBodyConfigID -> vehicle_to_body_config_id
      VIN -> vin
    """
    parts = _TOKEN_RE.findall(name)
    normalized = []
    for p in parts:
        if p.upper() in ACRONYMS:
            normalized.append(p.lower())
        else:
            normalized.append(p.lower())
    return "_".join([p for p in normalized if p])


def safe_identifier(name: str) -> str:
    """
    Return a safe python identifier (snake_case + keyword-safe).
    Accepts either CamelCase or snake_case.
    """
    snake = name if "_" in name else camel_to_snake(name)
    if is_reserved_identifier(snake):
        return f"{snake}_"
    return snake
