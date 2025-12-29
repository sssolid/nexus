from __future__ import annotations

import json
import logging
from collections import defaultdict, Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Type, Tuple, Iterable

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction
from django.db import models
from django.utils import timezone

from apps.autocare.core.models import AutocareRawRecord
from apps.autocare.vcdb.vcdb_plan import VCDB_INGEST_PLAN, VCDBPlanItem
from apps.autocare.vcdb.deps import topo_sort_models

# Optional import: only used when UI hydration is enabled.
# Keep in file so this remains a single drop-in command.
from apps.autocare.vcdb.vehicle_resolver import VehicleResolver
from apps.autocare.api import AutocareAPIClient


# ============================================================
# FILE LOGS
# ============================================================

ERROR_LOG_PATH = Path("/tmp/autocare_vcdb_ingest_errors.log")      # integrity / not-null / fatal issues
SKIP_LOG_PATH = Path("/tmp/autocare_vcdb_ingest_skips.jsonl")      # rows we intentionally skipped
SUMMARY_PATH = Path("/tmp/autocare_vcdb_ingest_summary.log")       # end-of-run summary

for p in (ERROR_LOG_PATH, SKIP_LOG_PATH, SUMMARY_PATH):
    p.parent.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("autocare.vcdb.ingest")
logger.setLevel(logging.INFO)

error_handler = logging.FileHandler(ERROR_LOG_PATH)
error_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logger.addHandler(error_handler)

skip_logger = logging.getLogger("autocare.vcdb.skips")
skip_logger.setLevel(logging.INFO)
skip_handler = logging.FileHandler(SKIP_LOG_PATH)
skip_handler.setFormatter(logging.Formatter("%(message)s"))
skip_logger.addHandler(skip_handler)

summary_logger = logging.getLogger("autocare.vcdb.summary")
summary_logger.setLevel(logging.INFO)
summary_handler = logging.FileHandler(SUMMARY_PATH)
summary_handler.setFormatter(logging.Formatter("%(message)s"))
summary_logger.addHandler(summary_handler)


# ============================================================
# TYPES
# ============================================================

@dataclass
class SkipRecord:
    reason: str
    model: str
    endpoint: str
    log_id: int
    row_index: int
    keys: dict[str, Any]
    raw_row: dict[str, Any]

    def to_json(self) -> str:
        return json.dumps(
            {
                "reason": self.reason,
                "model": self.model,
                "endpoint": self.endpoint,
                "log_id": self.log_id,
                "row_index": self.row_index,
                "keys": self.keys,
                "raw_row": self.raw_row,
            },
            default=str,
        )


# ============================================================
# HELPERS
# ============================================================

def resolve_model(app_label: str, model_name: str) -> Optional[Type[models.Model]]:
    try:
        return apps.get_model(app_label, model_name)
    except Exception:
        return None


def is_required_field(field: models.Field) -> bool:
    """
    Required: not null, no default.
    Auto PKs are not required.
    """
    if getattr(field, "null", False):
        return False
    if field.has_default():
        return False
    if getattr(field, "primary_key", False) and field.get_internal_type() in ("AutoField", "BigAutoField"):
        return False
    return True


def normalize_value(v: Any) -> Any:
    if v == "null":
        return None
    if isinstance(v, str) and "T" in v:
        try:
            dt = datetime.fromisoformat(v)
            # Make aware if project uses tz support and dt is naive.
            if timezone.is_naive(dt) and timezone.is_aware(timezone.now()):
                return timezone.make_aware(dt, timezone.get_current_timezone())
            return dt
        except ValueError:
            return v
    return v


def build_column_map(model: Type[models.Model]) -> Dict[str, str]:
    """
    db_column -> django attribute
    FK columns map to <field>_id so integers can be assigned (NOT model instances).
    """
    mapping: Dict[str, str] = {}
    for field in model._meta.fields:
        db_col = getattr(field, "db_column", None)
        if not db_col:
            continue
        if field.is_relation and field.many_to_one:
            mapping[db_col] = field.attname  # e.g. base_vehicle_id, engine_config2_id
        else:
            mapping[db_col] = field.name
    return mapping


def required_db_columns(model: Type[models.Model]) -> List[str]:
    cols = []
    for field in model._meta.fields:
        db_col = getattr(field, "db_column", None)
        if not db_col:
            continue
        if is_required_field(field):
            cols.append(db_col)
    return cols


def safe_row_dump(obj: models.Model) -> dict[str, Any]:
    """
    Never dereference FK objects.
    f.attname returns the raw underlying column value for FK fields.
    """
    return {f.name: getattr(obj, f.attname) for f in obj._meta.fields}


def chunked(seq: list[Any], size: int) -> Iterable[list[Any]]:
    for i in range(0, len(seq), size):
        yield seq[i:i + size]


# ============================================================
# SKIP / HYDRATION POLICY
# ============================================================

def _vehicle_fk_fields(model: Type[models.Model]) -> list[models.ForeignKey]:
    """
    Return FK fields on model that point to Vehicle.
    """
    vehicle_fk_fields: list[models.ForeignKey] = []
    try:
        VehicleModel = apps.get_model(model._meta.app_label, "Vehicle")
    except Exception:
        return []

    for f in model._meta.fields:
        if not (getattr(f, "is_relation", False) and getattr(f, "many_to_one", False)):
            continue
        rel_model = getattr(getattr(f, "remote_field", None), "model", None)
        if rel_model == VehicleModel:
            vehicle_fk_fields.append(f)
    return vehicle_fk_fields


def filter_rows_missing_vehicle(
    model: Type[models.Model],
    endpoint: str,
    log_id: int,
    instances_with_meta: list[tuple[int, dict[str, Any], models.Model]],
) -> tuple[list[tuple[int, dict[str, Any], models.Model]], list[SkipRecord]]:
    """
    Remove rows whose Vehicle FK references do not exist.
    This is the “skip the shittastic vehicle” mechanism — generalized.
    """
    fks = _vehicle_fk_fields(model)
    if not fks:
        return instances_with_meta, []

    VehicleModel = apps.get_model(model._meta.app_label, "Vehicle")

    referenced: set[int] = set()
    for _, _, obj in instances_with_meta:
        for fk in fks:
            vid = getattr(obj, fk.attname)
            if vid is not None:
                referenced.add(int(vid))

    if not referenced:
        return instances_with_meta, []

    existing = set(
        VehicleModel.objects.filter(vehicle_id__in=referenced).values_list("vehicle_id", flat=True)
    )

    kept: list[tuple[int, dict[str, Any], models.Model]] = []
    skipped: list[SkipRecord] = []

    for row_index, raw_row, obj in instances_with_meta:
        missing_vid: Optional[int] = None
        for fk in fks:
            vid = getattr(obj, fk.attname)
            if vid is not None and int(vid) not in existing:
                missing_vid = int(vid)
                break

        if missing_vid is not None:
            skipped.append(
                SkipRecord(
                    reason="MISSING_VEHICLE_FK",
                    model=model.__name__,
                    endpoint=endpoint,
                    log_id=log_id,
                    row_index=row_index,
                    keys={"VehicleID": missing_vid},
                    raw_row=raw_row,
                )
            )
        else:
            kept.append((row_index, raw_row, obj))

    return kept, skipped


def filter_rows_missing_engine_config2(
    model: Type[models.Model],
    endpoint: str,
    log_id: int,
    instances_with_meta: list[tuple[int, dict[str, Any], models.Model]],
) -> tuple[list[tuple[int, dict[str, Any], models.Model]], list[SkipRecord]]:
    """
    Specifically addresses your current issue:
    VehicleToEngineConfig references EngineConfigID values that exist in EngineConfig,
    but not in EngineConfig2. If your model FK points to EngineConfig2, those rows must be skipped.

    We only apply this for models that actually have an FK field named engine_config2 (attname engine_config2_id).
    """
    # fast check: model has field engine_config2 or engine_config2_id
    has_engine_config2_fk = any(
        f.is_relation and getattr(f, "many_to_one", False) and f.attname == "engine_config2_id"
        for f in model._meta.fields
    )
    if not has_engine_config2_fk:
        return instances_with_meta, []

    try:
        EngineConfig2Model = apps.get_model(model._meta.app_label, "EngineConfig2")
    except Exception:
        # If model exists but EngineConfig2 model doesn't, we can't validate; do not filter here.
        return instances_with_meta, []

    referenced: set[int] = set()
    for _, _, obj in instances_with_meta:
        eid = getattr(obj, "engine_config2_id", None)
        if eid is not None:
            referenced.add(int(eid))

    if not referenced:
        return instances_with_meta, []

    existing = set(
        EngineConfig2Model.objects.filter(engine_config_id__in=referenced).values_list("engine_config_id", flat=True)
    )

    kept: list[tuple[int, dict[str, Any], models.Model]] = []
    skipped: list[SkipRecord] = []

    for row_index, raw_row, obj in instances_with_meta:
        eid = getattr(obj, "engine_config2_id", None)
        if eid is not None and int(eid) not in existing:
            skipped.append(
                SkipRecord(
                    reason="MISSING_ENGINECONFIG2_FK",
                    model=model.__name__,
                    endpoint=endpoint,
                    log_id=log_id,
                    row_index=row_index,
                    keys={
                        "VehicleID": getattr(obj, "vehicle_id", None),
                        "EngineConfigID": int(eid),
                    },
                    raw_row=raw_row,
                )
            )
        else:
            kept.append((row_index, raw_row, obj))

    return kept, skipped


def maybe_hydrate_missing_vehicles(
    model: Type[models.Model],
    endpoint: str,
    log_id: int,
    instances: list[models.Model],
    resolver: VehicleResolver,
) -> None:
    """
    Optional: try to fetch and insert missing Vehicles prior to inserting child tables.

    This must be conservative — if your local Vehicle table has NOT NULL columns
    (SubmodelID/RegionID/etc), then creating a stub row is *not allowed* and will violate NOT NULL.
    So hydration must only create a Vehicle if it can populate all required fields.

    If resolver cannot, it should raise; we catch upstream and decide to skip instead.
    """
    fks = _vehicle_fk_fields(model)
    if not fks:
        return

    VehicleModel = apps.get_model(model._meta.app_label, "Vehicle")

    referenced: set[int] = set()
    for obj in instances:
        for fk in fks:
            vid = getattr(obj, fk.attname)
            if vid is not None:
                referenced.add(int(vid))

    if not referenced:
        return

    existing = set(
        VehicleModel.objects.filter(vehicle_id__in=referenced).values_list("vehicle_id", flat=True)
    )
    missing = sorted(referenced - existing)

    for vid in missing:
        # VehicleResolver is expected to create a valid Vehicle row or raise.
        resolver.ensure_vehicle_exists(VehicleModel, vid)


# ============================================================
# MANAGEMENT COMMAND
# ============================================================

class Command(BaseCommand):
    help = (
        "STRICT VCDB ingest.\n"
        "- Inserts raw payloads into models using db_column mapping\n"
        "- Logs exact failing rows\n"
        "- Can skip rows with missing Vehicle / EngineConfig2 FKs\n"
        "- Final summary includes skipped counts + file paths\n"
    )

    def add_arguments(self, parser):
        parser.add_argument("--app-label", default="autocare")
        parser.add_argument("--db", default="vcdb")
        parser.add_argument("--since", default=None)
        parser.add_argument("--asof", default=None)
        parser.add_argument("--endpoint", default=None)
        parser.add_argument("--batch-size", type=int, default=5000)

        parser.add_argument(
            "--order",
            choices=["explicit", "auto_fk"],
            default="auto_fk",
            help="explicit = VCDB_INGEST_PLAN order; auto_fk = topo sort by FK graph",
        )

        # Hydration is optional; skipping is usually what you want given your Vehicle NOT NULL constraints.
        parser.add_argument(
            "--ui-vehicle-lookup",
            action="store_true",
            help="Attempt to hydrate missing Vehicles via authenticated UI lookup endpoint before insert.",
        )

        # Skip switches (your request)
        parser.add_argument(
            "--skip-missing-vehicles",
            action="store_true",
            help="Skip rows whose Vehicle FK references are missing (and log them).",
        )
        parser.add_argument(
            "--skip-missing-engineconfig2",
            action="store_true",
            help="Skip rows whose EngineConfig2 FK references are missing (legacy EngineConfig), and log them.",
        )

        # Safety: clear existing data if desired (you requested earlier).
        parser.add_argument(
            "--truncate-first",
            action="store_true",
            help="DANGEROUS: Deletes data for all models in scope (in reverse order) before ingest.",
        )

    # --------------------------------------------------------

    def handle(self, *args, **opts):
        app_label: str = opts["app_label"]
        batch_size: int = opts["batch_size"]

        # Clear previous skip log on each run for clarity
        SKIP_LOG_PATH.write_text("")
        SUMMARY_PATH.write_text("")

        # Resolver only used if ui lookup enabled
        resolver: Optional[VehicleResolver] = None
        if opts["ui_vehicle_lookup"]:
            resolver = VehicleResolver(AutocareAPIClient())

        plan_items = [
            p for p in VCDB_INGEST_PLAN
            if opts["endpoint"] is None or p.endpoint == opts["endpoint"]
        ]

        existing_plan: List[VCDBPlanItem] = []
        for p in plan_items:
            if resolve_model(app_label, p.model) is None:
                self.stderr.write(f"⚠ Missing model for {p.endpoint}: {p.model}")
                continue
            existing_plan.append(p)

        if not existing_plan:
            self.stdout.write("No ingestable endpoints found.")
            return

        # Order: explicit = as you defined; auto_fk = topological sort.
        if opts["order"] == "explicit":
            ordered = existing_plan
        else:
            model_names = [p.model for p in existing_plan]
            sorted_models = topo_sort_models(app_label, model_names)
            index = {m: i for i, m in enumerate(sorted_models)}
            ordered = sorted(existing_plan, key=lambda p: index.get(p.model, 10**9))

        # Optional truncate (reverse order so children deleted first)
        if opts["truncate_first"]:
            self._truncate_models(app_label, ordered)

        qs = (
            AutocareRawRecord.objects
            .filter(source_db=opts["db"], record_count__gt=0)
            .order_by("fetched_at", "id")
        )
        if opts["since"]:
            qs = qs.filter(since_date=opts["since"])
        if opts["asof"]:
            qs = qs.filter(as_of_date=opts["asof"])

        logs_by_endpoint = defaultdict(list)
        for log in qs:
            logs_by_endpoint[log.endpoint].append(log)

        skip_counts = Counter()

        for item in ordered:
            model = resolve_model(app_label, item.model)
            logs = logs_by_endpoint.get(item.endpoint, [])

            if not logs:
                self.stdout.write(f"{item.endpoint}: no raw data")
                continue

            self.stdout.write(f"\n▶ {item.endpoint} → {item.model}")

            for log in logs:
                skipped = self._ingest_log_strict(
                    model=model,
                    log=log,
                    batch_size=batch_size,
                    resolver=resolver,
                    skip_missing_vehicles=opts["skip_missing_vehicles"],
                    skip_missing_engineconfig2=opts["skip_missing_engineconfig2"],
                )
                for s in skipped:
                    skip_counts[s.reason] += 1

        # End summary
        summary_logger.info("===== VCDB INGEST SUMMARY =====")
        summary_logger.info(f"Errors log:  {ERROR_LOG_PATH}")
        summary_logger.info(f"Skips log:   {SKIP_LOG_PATH}")
        summary_logger.info(f"Summary log: {SUMMARY_PATH}")
        summary_logger.info("")
        summary_logger.info("Skipped counts:")
        if skip_counts:
            for k, v in skip_counts.most_common():
                summary_logger.info(f"  - {k}: {v}")
        else:
            summary_logger.info("  (none)")

        self.stdout.write("\n✔ VCDB INGEST COMPLETE")
        self.stdout.write(f"• Errors: {ERROR_LOG_PATH}")
        self.stdout.write(f"• Skips:  {SKIP_LOG_PATH}")
        self.stdout.write(f"• Summary:{SUMMARY_PATH}")

    # --------------------------------------------------------

    def _truncate_models(self, app_label: str, ordered: list[VCDBPlanItem]) -> None:
        """
        Deletes data for selected models in reverse order.
        This avoids FK delete violations (children first).
        """
        self.stdout.write("\n⚠ TRUNCATE-FIRST ENABLED: deleting existing data for selected endpoints...")
        models_in_order: list[Type[models.Model]] = []
        for item in ordered:
            m = resolve_model(app_label, item.model)
            if m:
                models_in_order.append(m)

        for m in reversed(models_in_order):
            try:
                with transaction.atomic():
                    deleted, _ = m.objects.all().delete()
                self.stdout.write(f"  ✔ deleted {deleted} rows from {m._meta.db_table}")
            except Exception as exc:
                logger.error(json.dumps({
                    "error": "TRUNCATE_FAILED",
                    "model": m.__name__,
                    "db_table": m._meta.db_table,
                    "exception": str(exc),
                }, default=str))
                raise

    # --------------------------------------------------------

    def _ingest_log_strict(
        self,
        model: Type[models.Model],
        log: AutocareRawRecord,
        batch_size: int,
        resolver: Optional[VehicleResolver],
        skip_missing_vehicles: bool,
        skip_missing_engineconfig2: bool,
    ) -> list[SkipRecord]:
        payload = log.payload
        if isinstance(payload, str):
            payload = json.loads(payload)

        if not isinstance(payload, list):
            raise RuntimeError(f"Payload is not a list (log_id={log.id})")

        col_map = build_column_map(model)
        required = set(required_db_columns(model))

        # Build objects with metadata so we can skip + log accurately
        instances_with_meta: list[tuple[int, dict[str, Any], models.Model]] = []
        skipped_records: list[SkipRecord] = []

        for idx, row in enumerate(payload):
            if not isinstance(row, dict):
                continue

            # Case-insensitive input dict
            lower = {str(k).lower(): v for k, v in row.items()}
            data: Dict[str, Any] = {}
            missing_cols: list[str] = []

            for db_col, attr in col_map.items():
                v = normalize_value(lower.get(db_col.lower()))
                if v is None and db_col in required:
                    missing_cols.append(db_col)
                data[attr] = v

            if missing_cols:
                error = {
                    "error": "NOT_NULL_VIOLATION",
                    "model": model.__name__,
                    "endpoint": log.endpoint,
                    "log_id": log.id,
                    "row_index": idx,
                    "missing_columns": missing_cols,
                    "raw_row": row,
                    "mapped_data": data,
                }
                logger.error(json.dumps(error, default=str))
                raise RuntimeError(
                    f"NOT NULL violation in {model.__name__} "
                    f"(endpoint={log.endpoint}, log_id={log.id}, row={idx}). "
                    f"See {ERROR_LOG_PATH}"
                )

            instances_with_meta.append((idx, row, model(**data)))

        if not instances_with_meta:
            return []

        # --------------------------------------------------------
        # OPTIONAL VEHICLE HYDRATION (before filtering / insert)
        # --------------------------------------------------------
        if resolver is not None:
            # Hydrate based on the instance list (not meta)
            try:
                maybe_hydrate_missing_vehicles(
                    model=model,
                    endpoint=log.endpoint,
                    log_id=log.id,
                    instances=[obj for _, _, obj in instances_with_meta],
                    resolver=resolver,
                )
            except Exception as exc:
                # If hydration fails, you can still choose to skip missing vehicles.
                logger.error(json.dumps({
                    "error": "VEHICLE_HYDRATION_FAILED",
                    "model": model.__name__,
                    "endpoint": log.endpoint,
                    "log_id": log.id,
                    "exception": str(exc),
                }, default=str))

                # If skip is enabled, proceed to filter missing vehicles and keep going.
                # If skip is NOT enabled, stop here.
                if not skip_missing_vehicles:
                    raise RuntimeError(
                        f"Vehicle hydration failed for {model.__name__} "
                        f"(endpoint={log.endpoint}, log_id={log.id}). "
                        f"See {ERROR_LOG_PATH}"
                    ) from exc

        # --------------------------------------------------------
        # FILTER/SKIP: MISSING VEHICLE
        # --------------------------------------------------------
        if skip_missing_vehicles:
            instances_with_meta, skipped = filter_rows_missing_vehicle(
                model=model,
                endpoint=log.endpoint,
                log_id=log.id,
                instances_with_meta=instances_with_meta,
            )
            for s in skipped:
                skipped_records.append(s)
                skip_logger.info(s.to_json())

        # --------------------------------------------------------
        # FILTER/SKIP: MISSING ENGINECONFIG2 (legacy EngineConfig)
        # --------------------------------------------------------
        if skip_missing_engineconfig2:
            instances_with_meta, skipped = filter_rows_missing_engine_config2(
                model=model,
                endpoint=log.endpoint,
                log_id=log.id,
                instances_with_meta=instances_with_meta,
            )
            for s in skipped:
                skipped_records.append(s)
                skip_logger.info(s.to_json())

        # If everything was skipped, do not insert anything.
        if not instances_with_meta:
            self.stdout.write(f"  ⚠ {model.__name__}: inserted 0 rows (log {log.id}) — all skipped")
            return skipped_records

        instances = [obj for _, _, obj in instances_with_meta]

        # --------------------------------------------------------
        # INSERT (bulk, then isolate row on IntegrityError)
        # --------------------------------------------------------
        for chunk in chunked(instances, batch_size):
            try:
                with transaction.atomic():
                    model.objects.bulk_create(chunk)
            except IntegrityError as bulk_exc:
                # Bulk insert failed. Isolate failing row.
                for obj in chunk:
                    try:
                        with transaction.atomic():
                            obj.save(force_insert=True)
                    except IntegrityError as row_exc:
                        error = {
                            "error": "INTEGRITY_ERROR",
                            "model": model.__name__,
                            "db_table": model._meta.db_table,
                            "endpoint": log.endpoint,
                            "log_id": log.id,
                            "row_data": safe_row_dump(obj),
                            "exception": str(row_exc),
                        }
                        logger.error(json.dumps(error, default=str))
                        raise RuntimeError(
                            f"IntegrityError inserting {model.__name__} "
                            f"(endpoint={log.endpoint}, log_id={log.id}). "
                            f"See {ERROR_LOG_PATH}"
                        ) from row_exc

                raise RuntimeError(
                    f"Bulk IntegrityError in {model.__name__} but could not isolate row "
                    f"(endpoint={log.endpoint}, log_id={log.id})"
                ) from bulk_exc

        self.stdout.write(
            f"  ✔ {model.__name__}: inserted {len(instances)} rows (log {log.id}); "
            f"skipped {len(skipped_records)}"
        )
        return skipped_records
