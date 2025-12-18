from __future__ import annotations

import importlib
import pkgutil
from typing import Iterable


def import_submodules(package: str) -> list[str]:
    """
    Import all python modules under `package` (e.g. apps.autocare.models.vcdb).
    This ensures Django registers those models in the app registry.
    """
    imported: list[str] = []

    pkg = importlib.import_module(package)
    if not hasattr(pkg, "__path__"):
        return imported

    for mod in pkgutil.iter_modules(pkg.__path__, package + "."):
        # mod.name is the full dotted module path
        importlib.import_module(mod.name)
        imported.append(mod.name)

    return imported
