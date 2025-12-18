from __future__ import annotations

from collections import defaultdict, deque
from typing import Dict, List, Set, Tuple

from django.apps import apps
from django.db import models


def _model_label(model) -> str:
    return model.__name__


def build_fk_graph(app_label: str, model_names: List[str]) -> Tuple[Dict[str, Set[str]], Dict[str, Set[str]]]:
    """
    Build a graph using ONLY declared FK fields:
      edge A -> B means "A depends on B" (B must load first)

    This avoids accidentally using reverse relations, which commonly creates fake cycles.
    """
    deps: Dict[str, Set[str]] = {name: set() for name in model_names}
    rev: Dict[str, Set[str]] = {name: set() for name in model_names}

    name_set = set(model_names)

    for name in model_names:
        model = apps.get_model(app_label, name)

        for field in model._meta.fields:
            if not isinstance(field, models.ForeignKey):
                continue

            # Ignore self-FKs for ordering purposes; they don't prevent inserts if parent rows exist later.
            rel_model = field.remote_field.model
            if rel_model is None:
                continue

            rel_name = _model_label(rel_model)

            if rel_name == name:
                continue

            # Only consider dependencies within the same set we are sorting
            if rel_name in name_set:
                deps[name].add(rel_name)
                rev[rel_name].add(name)

    return deps, rev


def topo_sort_models(app_label: str, model_names: List[str]) -> List[str]:
    """
    Kahn topo sort. Raises ValueError if a *real* cycle remains.
    """
    deps, rev = build_fk_graph(app_label, model_names)

    indeg: Dict[str, int] = {n: len(deps[n]) for n in model_names}
    q = deque([n for n in model_names if indeg[n] == 0])

    out: List[str] = []
    while q:
        n = q.popleft()
        out.append(n)

        for child in rev.get(n, ()):
            indeg[child] -= 1
            if indeg[child] == 0:
                q.append(child)

    if len(out) != len(model_names):
        remaining = [n for n in model_names if n not in out]
        raise ValueError(f"FK cycle detected among: {remaining}")

    return out
