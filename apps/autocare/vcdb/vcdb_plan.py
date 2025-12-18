from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional


@dataclass(frozen=True)
class VCDBPlanItem:
    endpoint: str          # e.g. "/vcdb/Vehicle"
    model: str             # Django model class name, e.g. "Vehicle"
    group: str = ""        # optional label


VCDB_INGEST_PLAN: List[VCDBPlanItem] = [
    # Reference
    VCDBPlanItem("/vcdb/Year", "Year", "reference"),
    VCDBPlanItem("/vcdb/Make", "Make", "reference"),
    VCDBPlanItem("/vcdb/Region", "Region", "reference"),
    VCDBPlanItem("/vcdb/VehicleTypeGroup", "VehicleTypeGroup", "reference"),
    VCDBPlanItem("/vcdb/VehicleType", "VehicleType", "reference"),
    VCDBPlanItem("/vcdb/Class", "VehicleClass", "reference"),
    VCDBPlanItem("/vcdb/Model", "VehicleModel", "reference"),
    VCDBPlanItem("/vcdb/SubModel", "SubModel", "reference"),

    # Secondary reference / misc
    VCDBPlanItem("/vcdb/Abbreviation", "Abbreviation", "reference"),
    VCDBPlanItem("/vcdb/Mfr", "Mfr", "reference"),
    VCDBPlanItem("/vcdb/MfrBodyCode", "MfrBodyCode", "reference"),
    VCDBPlanItem("/vcdb/PublicationStage", "PublicationStage", "reference"),

    # Attributes
    VCDBPlanItem("/vcdb/DriveType", "DriveType", "attribute"),
    VCDBPlanItem("/vcdb/FuelType", "FuelType", "attribute"),
    VCDBPlanItem("/vcdb/TransmissionType", "TransmissionType", "attribute"),
    VCDBPlanItem("/vcdb/TransmissionControlType", "TransmissionControlType", "attribute"),
    VCDBPlanItem("/vcdb/TransmissionNumSpeeds", "TransmissionNumSpeeds", "attribute"),
    VCDBPlanItem("/vcdb/SteeringType", "SteeringType", "attribute"),
    VCDBPlanItem("/vcdb/SteeringSystem", "SteeringSystem", "attribute"),
    VCDBPlanItem("/vcdb/BrakeType", "BrakeType", "attribute"),
    VCDBPlanItem("/vcdb/BrakeSystem", "BrakeSystem", "attribute"),
    VCDBPlanItem("/vcdb/BrakeABS", "BrakeABS", "attribute"),
    VCDBPlanItem("/vcdb/SpringType", "SpringType", "attribute"),
    VCDBPlanItem("/vcdb/Valves", "Valves", "attribute"),
    VCDBPlanItem("/vcdb/Aspiration", "Aspiration", "attribute"),
    VCDBPlanItem("/vcdb/CylinderHeadType", "CylinderHeadType", "attribute"),
    VCDBPlanItem("/vcdb/BodyType", "BodyType", "attribute"),
    VCDBPlanItem("/vcdb/BodyNumDoors", "BodyNumDoors", "attribute"),
    VCDBPlanItem("/vcdb/BedType", "BedType", "attribute"),
    VCDBPlanItem("/vcdb/BedLength", "BedLength", "attribute"),
    VCDBPlanItem("/vcdb/WheelBase", "WheelBase", "attribute"),
    VCDBPlanItem("/vcdb/PowerOutput", "PowerOutput", "attribute"),
    VCDBPlanItem("/vcdb/IgnitionSystemType", "IgnitionSystemType", "attribute"),
    VCDBPlanItem("/vcdb/FuelDeliveryType", "FuelDeliveryType", "attribute"),
    VCDBPlanItem("/vcdb/FuelDeliverySubType", "FuelDeliverySubType", "attribute"),
    VCDBPlanItem("/vcdb/FuelSystemControlType", "FuelSystemControlType", "attribute"),
    VCDBPlanItem("/vcdb/FuelSystemDesign", "FuelSystemDesign", "attribute"),
    VCDBPlanItem("/vcdb/FuelDeliveryConfig", "FuelDeliveryConfig"),
    VCDBPlanItem("/vcdb/ElecControlled", "ElecControlled", "attribute"),

    # Config
    VCDBPlanItem("/vcdb/EngineBlock", "EngineBlock", "config"),
    VCDBPlanItem("/vcdb/EngineBoreStroke", "EngineBoreStroke", "config"),
    VCDBPlanItem("/vcdb/EngineBase", "EngineBase", "config"),
    VCDBPlanItem("/vcdb/EngineDesignation", "EngineDesignation", "config"),
    VCDBPlanItem("/vcdb/EngineVersion", "EngineVersion", "config"),
    VCDBPlanItem("/vcdb/EngineVIN", "EngineVIN", "config"),
    VCDBPlanItem("/vcdb/EngineConfig", "EngineConfig", "config"),
    VCDBPlanItem("/vcdb/TransmissionBase", "TransmissionBase", "config"),
    VCDBPlanItem("/vcdb/Transmission", "Transmission", "config"),
    VCDBPlanItem("/vcdb/TransmissionMfrCode", "TransmissionMfrCode", "config"),
    VCDBPlanItem("/vcdb/BrakeConfig", "BrakeConfig", "config"),
    VCDBPlanItem("/vcdb/SteeringConfig", "SteeringConfig", "config"),
    VCDBPlanItem("/vcdb/SpringTypeConfig", "SpringTypeConfig", "config"),
    VCDBPlanItem("/vcdb/BodyStyleConfig", "BodyStyleConfig", "config"),
    VCDBPlanItem("/vcdb/BedConfig", "BedConfig", "config"),

    # Core vehicles
    VCDBPlanItem("/vcdb/BaseVehicle", "BaseVehicle", "core"),
    VCDBPlanItem("/vcdb/Vehicle", "Vehicle", "core"),

    # Fitment
    VCDBPlanItem("/vcdb/VehicleToEngineConfig", "VehicleToEngineConfig", "fitment"),
    VCDBPlanItem("/vcdb/VehicleToTransmission", "VehicleToTransmission", "fitment"),
    VCDBPlanItem("/vcdb/VehicleToBodyConfig", "VehicleToBodyConfig", "fitment"),
    VCDBPlanItem("/vcdb/VehicleToBodyStyleConfig", "VehicleToBodyStyleConfig", "fitment"),
    VCDBPlanItem("/vcdb/VehicleToBrakeConfig", "VehicleToBrakeConfig", "fitment"),
    VCDBPlanItem("/vcdb/VehicleToSteeringConfig", "VehicleToSteeringConfig", "fitment"),
    VCDBPlanItem("/vcdb/VehicleToSpringTypeConfig", "VehicleToSpringTypeConfig", "fitment"),
    VCDBPlanItem("/vcdb/VehicleToDriveType", "VehicleToDriveType", "fitment"),
    VCDBPlanItem("/vcdb/VehicleToBedConfig", "VehicleToBedConfig", "fitment"),
    VCDBPlanItem("/vcdb/VehicleToWheelBase", "VehicleToWheelBase", "fitment"),
    VCDBPlanItem("/vcdb/VehicleToClass", "VehicleToClass", "fitment"),
    VCDBPlanItem("/vcdb/VehicleToMfrBodyCode", "VehicleToMfrBodyCode", "fitment"),

    # Change tracking
    VCDBPlanItem("/vcdb/VCdbChanges", "VCdbChanges", "changes"),
]


def plan_endpoints() -> List[str]:
    return [p.endpoint for p in VCDB_INGEST_PLAN]


def plan_model_for_endpoint(endpoint: str) -> Optional[str]:
    for p in VCDB_INGEST_PLAN:
        if p.endpoint == endpoint:
            return p.model
    return None
