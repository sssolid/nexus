VCDB_BASELINE_AS_OF = "2025-12-18"
DEFAULT_PAGE_SIZE = 1000

VCDB_BASELINE_PLAN = [
    # =========================
    # Reference tables
    # =========================
    "/vcdb/Year",
    "/vcdb/Make",
    "/vcdb/VehicleTypeGroup",
    "/vcdb/VehicleType",
    "/vcdb/Class",
    "/vcdb/Model",
    "/vcdb/SubModel",
    "/vcdb/Region",
    "/vcdb/Abbreviation",
    "/vcdb/PublicationStage",
    "/vcdb/Mfr",
    "/vcdb/MfrBodyCode",
    "/vcdb/BodyType",
    "/vcdb/BodyNumDoors",
    "/vcdb/BedType",
    "/vcdb/BedLength",
    "/vcdb/WheelBase",
    "/vcdb/Transmission",
    "/vcdb/TransmissionMfrCode",
    "/vcdb/ElecControlled",
    "/vcdb/PowerOutput",

    # =========================
    # Attribute tables
    # =========================
    "/vcdb/DriveType",
    "/vcdb/FuelType",
    "/vcdb/TransmissionType",
    "/vcdb/TransmissionControlType",
    "/vcdb/TransmissionNumSpeeds",
    "/vcdb/SteeringType",
    "/vcdb/SteeringSystem",
    "/vcdb/BrakeType",
    "/vcdb/BrakeSystem",
    "/vcdb/BrakeABS",
    "/vcdb/SpringType",
    "/vcdb/Valves",
    "/vcdb/Aspiration",
    "/vcdb/CylinderHeadType",

    # =========================
    # Configuration tables
    # =========================
    "/vcdb/EngineBlock",
    "/vcdb/EngineBoreStroke",
    "/vcdb/EngineBase",
    "/vcdb/EngineDesignation",
    "/vcdb/EngineVersion",
    "/vcdb/EngineVin",
    "/vcdb/FuelDeliveryType",
    "/vcdb/FuelDeliverySubType",
    "/vcdb/FuelDeliveryConfig",
    "/vcdb/FuelSystemControlType",
    "/vcdb/FuelSystemDesign",
    "/vcdb/IgnitionSystemType",
    "/vcdb/EngineConfig",
    "/vcdb/TransmissionBase",
    "/vcdb/BrakeConfig",
    "/vcdb/SteeringConfig",
    "/vcdb/SpringTypeConfig",
    "/vcdb/BodyStyleConfig",
    "/vcdb/BedConfig",

    # =========================
    # Core vehicles
    # =========================
    "/vcdb/BaseVehicle",
    "/vcdb/Vehicle",

    # =========================
    # Fitment tables (large)
    # =========================
    "/vcdb/VehicleToEngineConfig",
    "/vcdb/VehicleToTransmission",
    "/vcdb/VehicleToBodyConfig",
    "/vcdb/VehicleToDriveType",
    "/vcdb/VehicleToBedConfig",
    "/vcdb/VehicleToWheelBase",
    "/vcdb/VehicleToClass",
    "/vcdb/VehicleToBrakeConfig",
    "/vcdb/VehicleToBodyStyleConfig",
    "/vcdb/VehicleToSpringTypeConfig",
    "/vcdb/VehicleToSteeringConfig",
    "/vcdb/VehicleToMfrBodyCode",
]
