from __future__ import annotations

import json
import logging
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Type

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction
from django.db import models

from apps.autocare.models.base import AutocareRawRecord
from apps.autocare.vcdb.vcdb_plan import VCDB_INGEST_PLAN, VCDBPlanItem
from apps.autocare.vcdb.deps import topo_sort_models


LOG_PATH = Path("/tmp/autocare_vcdb_ingest_errors.log")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("autocare.vcdb.ingest")
logger.setLevel(logging.ERROR)
_handler = logging.FileHandler(LOG_PATH)
_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logger.addHandler(_handler)


def resolve_model(app_label: str, model_name: str) -> Optional[Type[models.Model]]:
    try:
        return apps.get_model(app_label, model_name)
    except Exception:
        return None


def is_required_field(field: models.Field) -> bool:
    if getattr(field, "null", False):
        return False
    if field.has_default():
        return False
    # Auto-created implicit PK is not required from payload
    if getattr(field, "primary_key", False) and field.get_internal_type() in ("AutoField", "BigAutoField"):
        return False
    return True


def normalize_value(v: Any) -> Any:
    if v == "null":
        return None
    if isinstance(v, str) and "T" in v:
        try:
            return datetime.fromisoformat(v)
        except ValueError:
            return v
    return v


def build_column_map(model: Type[models.Model]) -> Dict[str, str]:
    """
    db_column -> django_attr
    For FKs: map to <field_name>_id so you can assign raw integer IDs.
    """
    m: Dict[str, str] = {}
    for field in model._meta.fields:
        db_col = getattr(field, "db_column", None)
        if not db_col:
            continue
        if field.is_relation and getattr(field, "many_to_one", False):
            m[db_col] = f"{field.name}_id"
        else:
            m[db_col] = field.name
    return m


def required_db_columns(model: Type[models.Model]) -> List[str]:
    cols = []
    for field in model._meta.fields:
        db_col = getattr(field, "db_column", None)
        if not db_col:
            continue
        if is_required_field(field):
            cols.append(db_col)
    return cols


class Command(BaseCommand):
    help = "Ingest VCDB raw payloads into canonical VCDB tables, FK-safe order, with hard error logging."

    def add_arguments(self, parser):
        parser.add_argument("--app-label", default="autocare")
        parser.add_argument("--db", default="vcdb")
        parser.add_argument("--since", default=None)
        parser.add_argument("--asof", default=None)
        parser.add_argument("--endpoint", default=None, help="Only ingest one endpoint, e.g. /vcdb/Vehicle")
        parser.add_argument("--batch-size", type=int, default=5000)
        parser.add_argument("--stop-on-error", action="store_true", default=True)

        parser.add_argument(
            "--order",
            choices=["explicit", "auto_fk"],
            default="auto_fk",
            help="explicit = VCDB_INGEST_PLAN order; auto_fk = topological FK order (recommended).",
        )

    def handle(self, *args, **opts):
        app_label = opts["app_label"]

        # Build endpoint->model mapping from single source of truth
        plan_items = [p for p in VCDB_INGEST_PLAN if (opts["endpoint"] is None or p.endpoint == opts["endpoint"])]

        # Filter plan to only models that actually exist (generator might be incomplete)
        existing: List[VCDBPlanItem] = []
        for p in plan_items:
            if resolve_model(app_label, p.model) is None:
                self.stderr.write(f"⚠ Model missing for {p.endpoint}: {p.model} (skipping)")
                continue
            existing.append(p)

        if not existing:
            self.stdout.write("No ingestable items found.")
            return

        # Determine ingest order
        if opts["order"] == "explicit":
            ordered = existing
        else:
            # Auto-FK order across the subset present
            model_names = [p.model for p in existing]
            sorted_models = topo_sort_models(app_label, model_names)
            index = {m: i for i, m in enumerate(sorted_models)}
            ordered = sorted(existing, key=lambda p: index[p.model])

        # Group raw logs by endpoint (chronological)
        qs = (
            AutocareRawRecord.objects
            .filter(source_db=opts["db"])
            .filter(record_count__gt=0)
            .order_by("fetched_at", "id")
        )
        if opts["since"] is not None:
            qs = qs.filter(since_date=opts["since"])
        if opts["asof"] is not None:
            qs = qs.filter(as_of_date=opts["asof"])

        logs_by_endpoint = defaultdict(list)
        for log in qs:
            logs_by_endpoint[log.endpoint].append(log)

        # Execute ingest
        for item in ordered:
            model = resolve_model(app_label, item.model)
            if model is None:
                continue

            logs = logs_by_endpoint.get(item.endpoint, [])
            if not logs:
                self.stdout.write(f"{item.endpoint}: no raw batches to ingest")
                continue

            self.stdout.write(f"▶ {item.endpoint} -> {item.model} ({len(logs)} raw batches)")

            for log in logs:
                try:
                    self.ingest_one_log(model, log, batch_size=opts["batch_size"])
                except Exception as exc:
                    self.stderr.write(f"✖ ERROR at endpoint={item.endpoint} log_id={log.id}: {exc}")
                    if opts["stop_on_error"]:
                        self.stderr.write(f"Error details logged to {LOG_PATH}")
                        raise

        self.stdout.write("✔ VCDB canonical ingest complete.")

    def ingest_one_log(self, model: Type[models.Model], log: AutocareRawRecord, batch_size: int) -> None:
        payload = log.payload
        if isinstance(payload, str):
            payload = json.loads(payload)

        if not isinstance(payload, list):
            raise RuntimeError(f"Payload is not a list (log_id={log.id}, endpoint={log.endpoint})")

        col_map = build_column_map(model)
        required = set(required_db_columns(model))

        # Case-insensitive key access (Autocare casing can vary)
        instances: List[models.Model] = []

        for idx, row in enumerate(payload):
            if not isinstance(row, dict):
                continue

            normalized_row = {str(k).lower(): v for k, v in row.items()}

            data: Dict[str, Any] = {}
            missing: List[str] = []

            for db_col, attr in col_map.items():
                v = normalized_row.get(db_col.lower())
                v = normalize_value(v)

                if v is None and db_col in required:
                    missing.append(db_col)

                data[attr] = v

            if missing:
                error_payload = {
                    "error": "NOT_NULL_VIOLATION",
                    "model": model.__name__,
                    "db_table": model._meta.db_table,
                    "endpoint": log.endpoint,
                    "log_id": log.id,
                    "row_index": idx,
                    "missing_columns": missing,
                    "raw_row": row,
                    "mapped_data": data,
                }
                logger.error(json.dumps(error_payload, default=str))
                raise RuntimeError(
                    f"Invalid VCDB payload: missing required columns {missing} "
                    f"(endpoint={log.endpoint}, log_id={log.id}, row={idx}). "
                    f"See {LOG_PATH}"
                )

            instances.append(model(**data))

        if not instances:
            return

        # Bulk insert in chunks, log integrity errors with context
        try:
            with transaction.atomic():
                for i in range(0, len(instances), batch_size):
                    model.objects.bulk_create(
                        instances[i:i + batch_size],
                        ignore_conflicts=True,
                    )
        except IntegrityError as exc:
            logger.error(json.dumps({
                "error": "INTEGRITY_ERROR",
                "model": model.__name__,
                "db_table": model._meta.db_table,
                "endpoint": log.endpoint,
                "log_id": log.id,
                "exception": str(exc),
            }, default=str))
            raise

        self.stdout.write(f"  ✔ {model.__name__}: inserted {len(instances)} rows (log {log.id})")
