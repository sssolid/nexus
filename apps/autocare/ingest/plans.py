from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence


# ============================================================
# Core spec types
# ============================================================

@dataclass(frozen=True)
class EndpointSpec:
    """
    Declarative specification for a single Autocare endpoint.
    """
    db: str                    # vcdb / pcdb / padb / qdb
    resource: str              # Year / Parts / MetaData / etc
    api_version: str           # v1 / v4
    django_model: Optional[str] = None  # optional mapping hint

    @property
    def key(self) -> str:
        # stable identity for resume/state tracking
        return f"{self.db}:{self.resource}"

    @property
    def request_path(self) -> str:
        # the actual request path used for API calls
        return f"/api/{self.api_version}/{self.db}/{self.resource}"


@dataclass(frozen=True)
class DatasetSpec:
    """
    Dataset-level metadata. Plans are EndpointSpec sequences.
    """
    name: str
    plan: Sequence[EndpointSpec]
    default_as_of: str
    supports_as_of: bool = True

    def validate(self) -> None:
        # Defensive: ensure plan is internally consistent
        for spec in self.plan:
            if spec.db != self.name:
                raise ValueError(
                    f"Plan mismatch: dataset '{self.name}' contains spec '{spec.key}'"
                )


# ============================================================
# Defaults
# ============================================================

DEFAULT_PAGE_SIZE = 1000

# Baseline as-of dates (keep these explicit and per-dataset)
VCDB_BASELINE_AS_OF = "2025-12-18"
PCDB_BASELINE_AS_OF = "2025-12-18"
PADB_BASELINE_AS_OF = "2025-12-18"
QDB_BASELINE_AS_OF = "2025-12-18"
BRAND_BASELINE_AS_OF = "2025-12-18"


# ============================================================
# Plans
# ============================================================

VCDB_BASELINE_PLAN: List[EndpointSpec] = [
    # Reference
    EndpointSpec("vcdb", "Year", "v1", "Year"),
    EndpointSpec("vcdb", "Make", "v1", "Make"),
    EndpointSpec("vcdb", "VehicleTypeGroup", "v1", "VehicleTypeGroup"),
    EndpointSpec("vcdb", "VehicleType", "v1", "VehicleType"),
    EndpointSpec("vcdb", "Class", "v1", "VehicleClass"),
    EndpointSpec("vcdb", "Model", "v1", "VehicleModel"),
    EndpointSpec("vcdb", "SubModel", "v1", "SubModel"),
    EndpointSpec("vcdb", "Region", "v1", "Region"),
    EndpointSpec("vcdb", "Abbreviation", "v1", "Abbreviation"),
    EndpointSpec("vcdb", "PublicationStage", "v1", "PublicationStage"),
    EndpointSpec("vcdb", "Mfr", "v1", "Manufacturer"),
    EndpointSpec("vcdb", "MfrBodyCode", "v1", "ManufacturerBodyCode"),
    EndpointSpec("vcdb", "BodyType", "v1", "BodyType"),
    EndpointSpec("vcdb", "BodyNumDoors", "v1", "BodyNumDoors"),
    EndpointSpec("vcdb", "BedType", "v1", "BedType"),
    EndpointSpec("vcdb", "BedLength", "v1", "BedLength"),
    EndpointSpec("vcdb", "WheelBase", "v1", "WheelBase"),
    EndpointSpec("vcdb", "Transmission", "v1", "Transmission"),
    EndpointSpec("vcdb", "TransmissionMfrCode", "v1", "TransmissionManufacturerCode"),
    EndpointSpec("vcdb", "ElecControlled", "v1", "ElecControlled"),
    EndpointSpec("vcdb", "PowerOutput", "v1", "PowerOutput"),

    # Attribute
    EndpointSpec("vcdb", "DriveType", "v1", "DriveType"),
    EndpointSpec("vcdb", "FuelType", "v1", "FuelType"),
    EndpointSpec("vcdb", "TransmissionType", "v1", "TransmissionType"),
    EndpointSpec("vcdb", "TransmissionControlType", "v1", "TransmissionControlType"),
    EndpointSpec("vcdb", "TransmissionNumSpeeds", "v1", "TransmissionNumSpeeds"),
    EndpointSpec("vcdb", "SteeringType", "v1", "SteeringType"),
    EndpointSpec("vcdb", "SteeringSystem", "v1", "SteeringSystem"),
    EndpointSpec("vcdb", "BrakeType", "v1", "BrakeType"),
    EndpointSpec("vcdb", "BrakeSystem", "v1", "BrakeSystem"),
    EndpointSpec("vcdb", "BrakeABS", "v1", "BrakeABS"),
    EndpointSpec("vcdb", "SpringType", "v1", "SpringType"),
    EndpointSpec("vcdb", "Valves", "v1", "Valves"),
    EndpointSpec("vcdb", "Aspiration", "v1", "Aspiration"),
    EndpointSpec("vcdb", "CylinderHeadType", "v1", "CylinderHeadType"),

    # Configuration
    EndpointSpec("vcdb", "EngineBlock", "v1", "EngineBlock"),
    EndpointSpec("vcdb", "EngineBoreStroke", "v1", "EngineBoreStroke"),
    EndpointSpec("vcdb", "EngineBase", "v1", "EngineBase"),
    EndpointSpec("vcdb", "EngineBase2", "v1", "EngineBase2"),
    EndpointSpec("vcdb", "EngineDesignation", "v1", "EngineDesignation"),
    EndpointSpec("vcdb", "EngineVersion", "v1", "EngineVersion"),
    EndpointSpec("vcdb", "EngineVIN", "v1", "EngineVIN"),
    EndpointSpec("vcdb", "FuelDeliveryType", "v1", "FuelDeliveryType"),
    EndpointSpec("vcdb", "FuelDeliverySubType", "v1", "FuelDeliverySubType"),
    EndpointSpec("vcdb", "FuelDeliveryConfig", "v1", "FuelDeliveryConfig"),
    EndpointSpec("vcdb", "FuelSystemControlType", "v1", "FuelSystemControlType"),
    EndpointSpec("vcdb", "FuelSystemDesign", "v1", "FuelSystemDesign"),
    EndpointSpec("vcdb", "IgnitionSystemType", "v1", "IgnitionSystemType"),
    EndpointSpec("vcdb", "EngineConfig", "v1", "EngineConfig"),
    EndpointSpec("vcdb", "EngineConfig2", "v1", "EngineConfig2"),
    EndpointSpec("vcdb", "TransmissionBase", "v1", "TransmissionBase"),
    EndpointSpec("vcdb", "BrakeConfig", "v1", "BrakeConfig"),
    EndpointSpec("vcdb", "SteeringConfig", "v1", "SteeringConfig"),
    EndpointSpec("vcdb", "SpringTypeConfig", "v1", "SpringTypeConfig"),
    EndpointSpec("vcdb", "BodyStyleConfig", "v1", "BodyStyleConfig"),
    EndpointSpec("vcdb", "BedConfig", "v1", "BedConfig"),

    # Core vehicles
    EndpointSpec("vcdb", "BaseVehicle", "v1", "BaseVehicle"),
    EndpointSpec("vcdb", "Vehicle", "v1", "Vehicle"),

    # Fitment
    EndpointSpec("vcdb", "VehicleToEngineConfig", "v1", "VehicleToEngineConfig"),
    EndpointSpec("vcdb", "VehicleToTransmission", "v1", "VehicleToTransmission"),
    EndpointSpec("vcdb", "VehicleToBodyConfig", "v1", "VehicleToBodyConfig"),
    EndpointSpec("vcdb", "VehicleToDriveType", "v1", "VehicleToDriveType"),
    EndpointSpec("vcdb", "VehicleToBedConfig", "v1", "VehicleToBedConfig"),
    EndpointSpec("vcdb", "VehicleToWheelBase", "v1", "VehicleToWheelBase"),
    EndpointSpec("vcdb", "VehicleToClass", "v1", "VehicleToClass"),
    EndpointSpec("vcdb", "VehicleToBrakeConfig", "v1", "VehicleToBrakeConfig"),
    EndpointSpec("vcdb", "VehicleToBodyStyleConfig", "v1", "VehicleToBodyStyleConfig"),
    EndpointSpec("vcdb", "VehicleToSpringTypeConfig", "v1", "VehicleToSpringTypeConfig"),
    EndpointSpec("vcdb", "VehicleToSteeringConfig", "v1", "VehicleToSteeringConfig"),
    EndpointSpec("vcdb", "VehicleToMfrBodyCode", "v1", "VehicleToManufacturerBodyCode"),
]


PCDB_PLAN: List[EndpointSpec] = [
    EndpointSpec("pcdb", "ACESCodedValues", "v1"),
    EndpointSpec("pcdb", "Alias", "v1"),
    EndpointSpec("pcdb", "Categories", "v1"),
    EndpointSpec("pcdb", "PartCategory", "v1"),
    EndpointSpec("pcdb", "PartPosition", "v1"),
    EndpointSpec("pcdb", "Parts", "v1"),
    EndpointSpec("pcdb", "PartsDescription", "v1"),
    EndpointSpec("pcdb", "PartsRelationship", "v1"),
    EndpointSpec("pcdb", "PartsSupersession", "v1"),
    EndpointSpec("pcdb", "PartsToAlias", "v1"),
    EndpointSpec("pcdb", "PartsToUse", "v1"),
    EndpointSpec("pcdb", "PIESCode", "v1"),
    EndpointSpec("pcdb", "PIESEXPICode", "v1"),
    EndpointSpec("pcdb", "PIESEXPIGroup", "v1"),
    EndpointSpec("pcdb", "PIESField", "v1"),
    EndpointSpec("pcdb", "PIESReferenceFieldCode", "v1"),
    EndpointSpec("pcdb", "PIESSegment", "v1"),
    EndpointSpec("pcdb", "Positions", "v1"),
    EndpointSpec("pcdb", "Subcategories", "v1"),
    EndpointSpec("pcdb", "Use", "v1"),
]


PADB_PLAN: List[EndpointSpec] = [
    EndpointSpec("padb", "MeasurementGroup", "v4"),
    EndpointSpec("padb", "MetaData", "v4"),
    EndpointSpec("padb", "MetaUOMCodeAssignment", "v4"),
    EndpointSpec("padb", "MetaUOMCodes", "v4"),
    EndpointSpec("padb", "PartAttributeAssignment", "v4"),
    EndpointSpec("padb", "PartAttributes", "v4"),
    EndpointSpec("padb", "PartAttributeStyle", "v4"),
    EndpointSpec("padb", "PartTypeStyle", "v4"),
    EndpointSpec("padb", "Style", "v4"),
    EndpointSpec("padb", "ValidValueAssignment", "v4"),
    EndpointSpec("padb", "ValidValues", "v4"),
]


QDB_PLAN: List[EndpointSpec] = [
    EndpointSpec("qdb", "GroupNumber", "v1"),
    EndpointSpec("qdb", "Qualifier", "v1"),
    EndpointSpec("qdb", "QualifierGroup", "v1"),
    EndpointSpec("qdb", "QualifierType", "v1"),
]

BRAND_PLAN: List[EndpointSpec] = [
    EndpointSpec("brand", "Brand", "v1"),
]


# ============================================================
# Dataset registry (single source of truth)
# ============================================================

DATASETS: Dict[str, DatasetSpec] = {
    "vcdb": DatasetSpec("vcdb", VCDB_BASELINE_PLAN, VCDB_BASELINE_AS_OF, supports_as_of=True),
    "pcdb": DatasetSpec("pcdb", PCDB_PLAN, PCDB_BASELINE_AS_OF, supports_as_of=True),
    "padb": DatasetSpec("padb", PADB_PLAN, PADB_BASELINE_AS_OF, supports_as_of=True),
    "qdb":  DatasetSpec("qdb",  QDB_PLAN,  QDB_BASELINE_AS_OF,  supports_as_of=True),
    "brand":  DatasetSpec("brand",  BRAND_PLAN,  BRAND_BASELINE_AS_OF,  supports_as_of=True),
}

for _ds in DATASETS.values():
    _ds.validate()


# ============================================================
# Lookup helpers
# ============================================================

ALL_SPECS: Dict[str, EndpointSpec] = {
    spec.key: spec
    for ds in DATASETS.values()
    for spec in ds.plan
}


def get_dataset(name: str) -> DatasetSpec:
    if name not in DATASETS:
        raise KeyError(f"Unknown dataset: {name}")
    return DATASETS[name]


def get_spec(key: str) -> EndpointSpec:
    if key not in ALL_SPECS:
        raise KeyError(f"Unknown endpoint key: {key}")
    return ALL_SPECS[key]
