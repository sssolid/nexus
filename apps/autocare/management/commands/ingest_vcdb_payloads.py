import json
from datetime import datetime
from collections import defaultdict

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.autocare.models import AutocareRawRecord
import logging
from pathlib import Path

LOG_PATH = Path("/var/log/django/autocare_vcdb_ingest.log")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("autocare.vcdb.ingest")
logger.setLevel(logging.ERROR)

handler = logging.FileHandler(LOG_PATH)
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logger.addHandler(handler)


# ============================================================
# Canonical VCDB ingestion plan (ORDER MATTERS)
# ============================================================

VCDB_INGEST_PLAN = [
    # ============================================================
    # Core reference tables (no dependencies)
    # ============================================================
    ("/vcdb/Year", "Year"),
    ("/vcdb/Make", "Make"),
    ("/vcdb/Region", "Region"),
    ("/vcdb/VehicleTypeGroup", "VehicleTypeGroup"),
    ("/vcdb/VehicleType", "VehicleType"),
    ("/vcdb/Class", "VehicleClass"),
    ("/vcdb/Model", "VehicleModel"),
    ("/vcdb/SubModel", "SubModel"),

    # ============================================================
    # Secondary reference tables
    # ============================================================
    ("/vcdb/Abbreviation", "Abbreviation"),
    ("/vcdb/Mfr", "Manufacturer"),
    ("/vcdb/MfrBodyCode", "ManufacturerBodyCode"),
    ("/vcdb/PublicationStage", "PublicationStage"),

    # ============================================================
    # Attribute tables
    # ============================================================
    ("/vcdb/DriveType", "DriveType"),
    ("/vcdb/FuelType", "FuelType"),
    ("/vcdb/TransmissionType", "TransmissionType"),
    ("/vcdb/TransmissionControlType", "TransmissionControlType"),
    ("/vcdb/TransmissionNumSpeeds", "TransmissionNumSpeeds"),
    ("/vcdb/SteeringType", "SteeringType"),
    ("/vcdb/SteeringSystem", "SteeringSystem"),
    ("/vcdb/BrakeType", "BrakeType"),
    ("/vcdb/BrakeSystem", "BrakeSystem"),
    ("/vcdb/BrakeABS", "BrakeABS"),
    ("/vcdb/SpringType", "SpringType"),
    ("/vcdb/Valves", "Valves"),
    ("/vcdb/Aspiration", "Aspiration"),
    ("/vcdb/CylinderHeadType", "CylinderHeadType"),
    ("/vcdb/BodyType", "BodyType"),
    ("/vcdb/BodyNumDoors", "BodyNumDoors"),
    ("/vcdb/BedType", "BedType"),
    ("/vcdb/BedLength", "BedLength"),
    ("/vcdb/WheelBase", "WheelBase"),
    ("/vcdb/PowerOutput", "PowerOutput"),
    ("/vcdb/IgnitionSystemType", "IgnitionSystemType"),
    ("/vcdb/FuelDeliveryType", "FuelDeliveryType"),
    ("/vcdb/FuelDeliverySubType", "FuelDeliverySubType"),
    ("/vcdb/FuelDeliveryConfig", "FuelDeliveryConfig"),
    ("/vcdb/FuelSystemControlType", "FuelSystemControlType"),
    ("/vcdb/FuelSystemDesign", "FuelSystemDesign"),
    ("/vcdb/ElecControlled", "ElecControlled"),

    # ============================================================
    # Engine / drivetrain configuration tables
    # ============================================================
    ("/vcdb/EngineBlock", "EngineBlock"),
    ("/vcdb/EngineBoreStroke", "EngineBoreStroke"),
    ("/vcdb/EngineBase", "EngineBase"),
    ("/vcdb/EngineDesignation", "EngineDesignation"),
    ("/vcdb/EngineVersion", "EngineVersion"),
    ("/vcdb/EngineVIN", "EngineVIN"),
    ("/vcdb/EngineConfig", "EngineConfig"),
    ("/vcdb/TransmissionBase", "TransmissionBase"),
    ("/vcdb/Transmission", "Transmission"),
    ("/vcdb/TransmissionMfrCode", "TransmissionManufacturerCode"),

    # ============================================================
    # Body / chassis configuration tables
    # ============================================================
    ("/vcdb/BrakeConfig", "BrakeConfig"),
    ("/vcdb/SteeringConfig", "SteeringConfig"),
    ("/vcdb/SpringTypeConfig", "SpringTypeConfig"),
    ("/vcdb/BodyStyleConfig", "BodyStyleConfig"),
    ("/vcdb/BedConfig", "BedConfig"),

    # ============================================================
    # Core vehicle entities (high volume)
    # ============================================================
    ("/vcdb/BaseVehicle", "BaseVehicle"),
    ("/vcdb/Vehicle", "Vehicle"),

    # ============================================================
    # Vehicle relationship / fitment tables (very large)
    # ============================================================
    ("/vcdb/VehicleToEngineConfig", "VehicleToEngineConfig"),
    ("/vcdb/VehicleToTransmission", "VehicleToTransmission"),
    ("/vcdb/VehicleToBodyConfig", "VehicleToBodyConfig"),
    ("/vcdb/VehicleToBodyStyleConfig", "VehicleToBodyStyleConfig"),
    ("/vcdb/VehicleToBrakeConfig", "VehicleToBrakeConfig"),
    ("/vcdb/VehicleToSteeringConfig", "VehicleToSteeringConfig"),
    ("/vcdb/VehicleToSpringTypeConfig", "VehicleToSpringTypeConfig"),
    ("/vcdb/VehicleToDriveType", "VehicleToDriveType"),
    ("/vcdb/VehicleToBedConfig", "VehicleToBedConfig"),
    ("/vcdb/VehicleToWheelBase", "VehicleToWheelBase"),
    ("/vcdb/VehicleToClass", "VehicleToClass"),
    ("/vcdb/VehicleToMfrBodyCode", "VehicleToManufacturerBodyCode"),

    # ============================================================
    # Change tracking
    # ============================================================
    ("/vcdb/VCdbChanges", "VCdbChanges"),
]


def resolve_vcdb_model(endpoint: str):
    for prefix, model_name in VCDB_INGEST_PLAN:
        if endpoint == model_name:
            model_name = apps.get_model("autocare", model_name)
            return model_name
    return None


# ============================================================
# Command
# ============================================================

class Command(BaseCommand):
    help = "Ingest VCDB API payloads into canonical VCDB tables in dependency order."

    def handle(self, *args, **options):
        # Group logs by endpoint, ordered chronologically
        logs_by_endpoint = defaultdict(list)

        qs = (
            AutocareRawRecord.objects
            .filter(record_count__gt=0)
            .order_by("fetched_at", "id")
        )

        for log in qs:
            logs_by_endpoint[log.endpoint].append(log)

        # Ingest by canonical order
        for endpoint, model_name in VCDB_INGEST_PLAN:
            model = resolve_vcdb_model(model_name)
            if model is None:
                self.stderr.write(f"⚠ No model found for {model_name} (endpoint {endpoint})")
                continue

            logs = logs_by_endpoint.get(endpoint, [])
            if not logs:
                continue

            self.stdout.write(f"▶ Ingesting {endpoint} → {model_name} ({len(logs)} batches)")

            for log in logs:
                self.ingest_log(model, log)

    @staticmethod
    def get_required_db_columns(model):
        """
        Return db_column names that are NOT NULL and have no default.
        """
        required = set()
        for field in model._meta.fields:
            if field.null:
                continue
            if field.primary_key:
                continue
            if field.has_default():
                continue
            if field.db_column:
                required.add(field.db_column)
        return required

    @staticmethod
    def is_required_field(field):
        """
        A field is required if:
        - It is NOT nullable
        - It has NO default
        - AND it is NOT an auto-generated PK
        """
        if field.null:
            return False

        if field.has_default():
            return False

        # AutoField / BigAutoField are generated by Django → not required
        if field.primary_key and field.get_internal_type() in ("AutoField", "BigAutoField"):
            return False

        return True

    def ingest_log(self, model, log):
        payload = log.payload
        if isinstance(payload, str):
            payload = json.loads(payload)

        if not isinstance(payload, list):
            raise RuntimeError(
                f"Payload is not a list (log_id={log.id}, endpoint={log.endpoint})"
            )

        # Build db_column → django attr map
        column_map = {}
        for field in model._meta.fields:
            if not field.db_column:
                continue
            if field.is_relation and field.many_to_one:
                column_map[field.db_column] = f"{field.name}_id"
            else:
                column_map[field.db_column] = field.name

        required_columns = {
            field.db_column
            for field in model._meta.fields
            if field.db_column and self.is_required_field(field)
        }

        instances = []

        for idx, row in enumerate(payload):
            data = {}
            missing = []

            # Normalize payload keys for case-insensitive matching
            normalized_row = {
                k.lower(): v
                for k, v in row.items()
            }

            for db_col, attr in column_map.items():
                value = normalized_row.get(db_col.lower())

                if value == "null":
                    value = None

                if value is None and db_col in required_columns:
                    missing.append(db_col)

                if isinstance(value, str) and "T" in value:
                    try:
                        value = datetime.fromisoformat(value)
                    except ValueError:
                        pass

                data[attr] = value

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
                    f"Invalid VCDB payload detected. "
                    f"See log file for details. "
                    f"(endpoint={log.endpoint}, log_id={log.id}, row={idx})"
                )

            instances.append(model(**data))

        if not instances:
            return

        with transaction.atomic():
            model.objects.bulk_create(instances, ignore_conflicts=True)

        self.stdout.write(
            f"✔ {model.__name__}: inserted {len(instances)} rows "
            f"(log {log.id})"
        )


