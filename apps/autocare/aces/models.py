from django.db import models


# =====================================================
# CORE APPLICATION RECORD
# =====================================================

class AcesApp(models.Model):
    """Core ACES application record"""
    source_file = models.TextField()
    app_id = models.BigIntegerField(db_index=True)

    action = models.CharField(max_length=1)
    validate = models.BooleanField(default=True)

    part_number = models.CharField(max_length=45, db_index=True)
    part_type_id = models.IntegerField(db_index=True)
    quantity = models.IntegerField(null=True)
    position_id = models.IntegerField(null=True)

    brand_aaiaid = models.CharField(max_length=4, null=True)
    subbrand_aaiaid = models.CharField(max_length=4, null=True)
    mfr_label = models.TextField(null=True)

    # Additional fields from ACES 4.2 spec
    display_order = models.IntegerField(null=True)
    asset_name = models.CharField(max_length=45, null=True)
    asset_item_order = models.IntegerField(null=True)
    asset_item_ref = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = '"autocare_aces"."app"'
        unique_together = [("source_file", "app_id")]
        indexes = [
            models.Index(fields=["part_number"]),
            models.Index(fields=["part_type_id"]),
        ]


# =====================================================
# VEHICLE AXIS
# =====================================================

class AcesAppVehicle(models.Model):
    """Vehicle identification and primary attributes"""
    app = models.OneToOneField(AcesApp, on_delete=models.CASCADE, primary_key=True)

    # base_vehicle_id = models.IntegerField(null=True, db_index=True)
    base_vehicle = models.ForeignKey(
        'autocare_vcdb.BaseVehicle',
        db_column='BaseVehicleID',
        to_field='base_vehicle_id',
        related_name='aces_applications',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
    # make_id = models.IntegerField(null=True, db_index=True)
    make = models.ForeignKey(
        'autocare_vcdb.Make',
        db_column='MakeID',
        to_field='make_id',
        related_name='aces_applications',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
    # model_id = models.IntegerField(null=True, db_index=True)
    model = models.ForeignKey(
        'autocare_vcdb.VehicleModel',
        db_column='ModelID',
        to_field='model_id',
        related_name='aces_applications',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
    # submodel_id = models.IntegerField(null=True, db_index=True)
    submodel = models.ForeignKey(
        'autocare_vcdb.SubModel',
        db_column='SubModelID',
        to_field='submodel_id',
        related_name='aces_applications',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )

    year_from = models.IntegerField(null=True, db_index=True)
    year_to = models.IntegerField(null=True, db_index=True)

    engine_base_id = models.IntegerField(null=True, db_index=True)
    engine_block_id = models.IntegerField(null=True, db_index=True)
    engine_vin_id = models.IntegerField(null=True, db_index=True)
    aspiration_id = models.IntegerField(null=True, db_index=True)

    transmission_base_id = models.IntegerField(null=True, db_index=True)
    transmission_type_id = models.IntegerField(null=True, db_index=True)

    # Additional commonly used attributes in vehicle axis
    drive_type_id = models.IntegerField(null=True, db_index=True)
    fuel_type_id = models.IntegerField(null=True, db_index=True)

    # Equipment identification
    equipment_base_id = models.IntegerField(null=True, db_index=True)
    equipment_model_id = models.IntegerField(null=True, db_index=True)
    mfr_id = models.IntegerField(null=True, db_index=True)

    # Production years for equipment
    production_year_start = models.IntegerField(null=True)
    production_year_end = models.IntegerField(null=True)

    class Meta:
        db_table = '"autocare_aces"."app_vehicle"'


# =====================================================
# ATTRIBUTE BASE CLASS
# =====================================================

class _AcesAttrBase(models.Model):
    """Base class for all attribute tables"""
    app = models.ForeignKey(AcesApp, on_delete=models.CASCADE)

    class Meta:
        abstract = True


# =====================================================
# BODY / CHASSIS ATTRIBUTES
# =====================================================

class AcesBodyType(_AcesAttrBase):
    body_type_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = '"autocare_aces"."body_type"'
        unique_together = [("app", "body_type_id")]


class AcesBodyNumDoors(_AcesAttrBase):
    body_num_doors_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = '"autocare_aces"."body_num_doors"'
        unique_together = [("app", "body_num_doors_id")]


class AcesBedType(_AcesAttrBase):
    bed_type_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = '"autocare_aces"."bed_type"'
        unique_together = [("app", "bed_type_id")]


class AcesBedLength(_AcesAttrBase):
    bed_length_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = '"autocare_aces"."bed_length"'
        unique_together = [("app", "bed_length_id")]


class AcesWheelBase(_AcesAttrBase):
    wheel_base_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = '"autocare_aces"."wheel_base"'
        unique_together = [("app", "wheel_base_id")]


# =====================================================
# BRAKING ATTRIBUTES
# =====================================================

class AcesBrakeAbs(_AcesAttrBase):
    brake_abs_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = '"autocare_aces"."brake_abs"'
        unique_together = [("app", "brake_abs_id")]


class AcesBrakeSystem(_AcesAttrBase):
    brake_system_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = '"autocare_aces"."brake_system"'
        unique_together = [("app", "brake_system_id")]


class AcesFrontBrakeType(_AcesAttrBase):
    front_brake_type_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = '"autocare_aces"."front_brake_type"'
        unique_together = [("app", "front_brake_type_id")]


class AcesRearBrakeType(_AcesAttrBase):
    rear_brake_type_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = '"autocare_aces"."rear_brake_type"'
        unique_together = [("app", "rear_brake_type_id")]


# =====================================================
# DRIVETRAIN / STEERING ATTRIBUTES
# =====================================================

class AcesDriveType(_AcesAttrBase):
    drive_type_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = '"autocare_aces"."drive_type"'
        unique_together = [("app", "drive_type_id")]


class AcesSteeringSystem(_AcesAttrBase):
    steering_system_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = '"autocare_aces"."steering_system"'
        unique_together = [("app", "steering_system_id")]


class AcesSteeringType(_AcesAttrBase):
    steering_type_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = '"autocare_aces"."steering_type"'
        unique_together = [("app", "steering_type_id")]


# =====================================================
# SUSPENSION ATTRIBUTES
# =====================================================

class AcesFrontSpringType(_AcesAttrBase):
    front_spring_type_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = '"autocare_aces"."front_spring_type"'
        unique_together = [("app", "front_spring_type_id")]


class AcesRearSpringType(_AcesAttrBase):
    rear_spring_type_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = '"autocare_aces"."rear_spring_type"'
        unique_together = [("app", "rear_spring_type_id")]


# =====================================================
# ENGINE CORE ATTRIBUTES
# =====================================================

class AcesEngineBase(_AcesAttrBase):
    engine_base_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = '"autocare_aces"."engine_base"'
        unique_together = [("app", "engine_base_id")]


class AcesEngineBlock(_AcesAttrBase):
    engine_block_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = '"autocare_aces"."engine_block"'
        unique_together = [("app", "engine_block_id")]


class AcesEngineBoreStroke(_AcesAttrBase):
    engine_bore_stroke_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = '"autocare_aces"."engine_bore_stroke"'
        unique_together = [("app", "engine_bore_stroke_id")]


class AcesEngineDesignation(_AcesAttrBase):
    engine_designation_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = '"autocare_aces"."engine_designation"'
        unique_together = [("app", "engine_designation_id")]


class AcesEngineVin(_AcesAttrBase):
    engine_vin_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = '"autocare_aces"."engine_vin"'
        unique_together = [("app", "engine_vin_id")]


class AcesEngineVersion(_AcesAttrBase):
    engine_version_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = '"autocare_aces"."engine_version"'
        unique_together = [("app", "engine_version_id")]


class AcesEngineMfr(_AcesAttrBase):
    engine_mfr_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = '"autocare_aces"."engine_mfr"'
        unique_together = [("app", "engine_mfr_id")]


class AcesCylinderHeadType(_AcesAttrBase):
    cylinder_head_type_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = '"autocare_aces"."cylinder_head_type"'
        unique_together = [("app", "cylinder_head_type_id")]


# =====================================================
# FUEL / IGNITION ATTRIBUTES
# =====================================================

class AcesFuelType(_AcesAttrBase):
    fuel_type_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = '"autocare_aces"."fuel_type"'
        unique_together = [("app", "fuel_type_id")]


class AcesFuelDeliveryType(_AcesAttrBase):
    fuel_delivery_type_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = '"autocare_aces"."fuel_delivery_type"'
        unique_together = [("app", "fuel_delivery_type_id")]


class AcesFuelDeliverySubType(_AcesAttrBase):
    fuel_delivery_sub_type_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = '"autocare_aces"."fuel_delivery_sub_type"'
        unique_together = [("app", "fuel_delivery_sub_type_id")]


class AcesFuelSystemControlType(_AcesAttrBase):
    fuel_system_control_type_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = '"autocare_aces"."fuel_system_control_type"'
        unique_together = [("app", "fuel_system_control_type_id")]


class AcesFuelSystemDesign(_AcesAttrBase):
    fuel_system_design_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = '"autocare_aces"."fuel_system_design"'
        unique_together = [("app", "fuel_system_design_id")]


class AcesIgnitionSystemType(_AcesAttrBase):
    ignition_system_type_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = '"autocare_aces"."ignition_system_type"'
        unique_together = [("app", "ignition_system_type_id")]


# =====================================================
# POWERTRAIN ATTRIBUTES
# =====================================================

class AcesAspiration(_AcesAttrBase):
    aspiration_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = '"autocare_aces"."aspiration"'
        unique_together = [("app", "aspiration_id")]


class AcesPowerOutput(_AcesAttrBase):
    power_output_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = '"autocare_aces"."power_output"'
        unique_together = [("app", "power_output_id")]


class AcesValvesPerEngine(_AcesAttrBase):
    valves_per_engine_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = '"autocare_aces"."valves_per_engine"'
        unique_together = [("app", "valves_per_engine_id")]


# =====================================================
# TRANSMISSION ATTRIBUTES
# =====================================================

class AcesTransmissionBase(_AcesAttrBase):
    transmission_base_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = '"autocare_aces"."transmission_base"'
        unique_together = [("app", "transmission_base_id")]


class AcesTransmissionType(_AcesAttrBase):
    transmission_type_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = '"autocare_aces"."transmission_type"'
        unique_together = [("app", "transmission_type_id")]


class AcesTransmissionControlType(_AcesAttrBase):
    transmission_control_type_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = '"autocare_aces"."transmission_control_type"'
        unique_together = [("app", "transmission_control_type_id")]


class AcesTransmissionNumSpeeds(_AcesAttrBase):
    transmission_num_speeds_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = '"autocare_aces"."transmission_num_speeds"'
        unique_together = [("app", "transmission_num_speeds_id")]


class AcesTransmissionMfr(_AcesAttrBase):
    transmission_mfr_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = '"autocare_aces"."transmission_mfr"'
        unique_together = [("app", "transmission_mfr_id")]


class AcesTransmissionMfrCode(_AcesAttrBase):
    transmission_mfr_code_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = '"autocare_aces"."transmission_mfr_code"'
        unique_together = [("app", "transmission_mfr_code_id")]


class AcesTransElecControlled(_AcesAttrBase):
    trans_elec_controlled_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = '"autocare_aces"."trans_elec_controlled"'
        unique_together = [("app", "trans_elec_controlled_id")]


# =====================================================
# EQUIPMENT ATTRIBUTES
# =====================================================

class AcesEquipmentBase(_AcesAttrBase):
    equipment_base_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = '"autocare_aces"."equipment_base"'
        unique_together = [("app", "equipment_base_id")]


class AcesEquipmentModel(_AcesAttrBase):
    equipment_model_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = '"autocare_aces"."equipment_model"'
        unique_together = [("app", "equipment_model_id")]


# =====================================================
# MANUFACTURER / REGION ATTRIBUTES
# =====================================================

class AcesMfr(_AcesAttrBase):
    mfr_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = '"autocare_aces"."mfr"'
        unique_together = [("app", "mfr_id")]


class AcesMfrBodyCode(_AcesAttrBase):
    mfr_body_code_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = '"autocare_aces"."mfr_body_code"'
        unique_together = [("app", "mfr_body_code_id")]


class AcesRegion(_AcesAttrBase):
    region_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = '"autocare_aces"."region"'
        unique_together = [("app", "region_id")]


# =====================================================
# VEHICLE TYPE (can be multiple per app)
# =====================================================

class AcesVehicleType(models.Model):
    """VehicleType can appear multiple times per app"""
    app = models.ForeignKey(AcesApp, on_delete=models.CASCADE, related_name='vehicle_types')
    vehicle_type_id = models.IntegerField(db_index=True)
    idx = models.IntegerField(default=0)  # Order in which it appeared

    class Meta:
        db_table = '"autocare_aces"."vehicle_type"'
        indexes = [
            models.Index(fields=["app", "idx"]),
            models.Index(fields=["vehicle_type_id"]),
        ]


# =====================================================
# QUALIFIERS
# =====================================================

class AcesQualifier(models.Model):
    """Qualifier records with text and parameters"""
    app = models.ForeignKey(AcesApp, on_delete=models.CASCADE, related_name='qualifiers')

    qual_id = models.IntegerField(db_index=True)
    qual_text = models.TextField(null=True)

    param_1 = models.TextField(null=True)
    param_2 = models.TextField(null=True)
    param_3 = models.TextField(null=True)

    class Meta:
        db_table = '"autocare_aces"."qualifier"'
        indexes = [models.Index(fields=["qual_id"])]


# =====================================================
# RAW ATTRIBUTE FALLBACK
# =====================================================

class AcesRawAttribute(models.Model):
    """
    Fallback storage for:
    1. Attributes that don't have typed tables yet
    2. Notes (stored with attr_name='note')
    3. Any unmapped data to ensure nothing is lost
    """
    app = models.ForeignKey(AcesApp, on_delete=models.CASCADE, related_name='raw_attributes')

    attr_name = models.CharField(max_length=64, db_index=True)
    attr_id = models.IntegerField(null=True)
    attr_value = models.TextField(null=True)
    idx = models.IntegerField(default=0)  # Order for repeated attributes

    class Meta:
        db_table = '"autocare_aces"."raw_attribute"'
        indexes = [
            models.Index(fields=["attr_name"]),
            models.Index(fields=["app", "attr_name", "idx"]),
        ]


# =====================================================
# ATTRIBUTE REGISTRY
# =====================================================

ACES_TYPED_TABLES = {
    # --- Body / Chassis ---
    "body_type": ("body_type_id", AcesBodyType),
    "body_num_doors": ("body_num_doors_id", AcesBodyNumDoors),
    "bed_type": ("bed_type_id", AcesBedType),
    "bed_length": ("bed_length_id", AcesBedLength),
    "wheel_base": ("wheel_base_id", AcesWheelBase),

    # --- Braking ---
    "brake_abs": ("brake_abs_id", AcesBrakeAbs),
    "brake_system": ("brake_system_id", AcesBrakeSystem),
    "front_brake_type": ("front_brake_type_id", AcesFrontBrakeType),
    "rear_brake_type": ("rear_brake_type_id", AcesRearBrakeType),

    # --- Suspension / Steering / Drivetrain ---
    "drive_type": ("drive_type_id", AcesDriveType),
    "steering_system": ("steering_system_id", AcesSteeringSystem),
    "steering_type": ("steering_type_id", AcesSteeringType),
    "front_spring_type": ("front_spring_type_id", AcesFrontSpringType),
    "rear_spring_type": ("rear_spring_type_id", AcesRearSpringType),

    # --- Engine Core ---
    "engine_base": ("engine_base_id", AcesEngineBase),
    "engine_block": ("engine_block_id", AcesEngineBlock),
    "engine_bore_stroke": ("engine_bore_stroke_id", AcesEngineBoreStroke),
    "engine_designation": ("engine_designation_id", AcesEngineDesignation),
    "engine_vin": ("engine_vin_id", AcesEngineVin),
    "engine_version": ("engine_version_id", AcesEngineVersion),
    "engine_mfr": ("engine_mfr_id", AcesEngineMfr),
    "cylinder_head_type": ("cylinder_head_type_id", AcesCylinderHeadType),

    # --- Fuel / Ignition ---
    "fuel_type": ("fuel_type_id", AcesFuelType),
    "fuel_delivery_type": ("fuel_delivery_type_id", AcesFuelDeliveryType),
    "fuel_delivery_sub_type": ("fuel_delivery_sub_type_id", AcesFuelDeliverySubType),
    "fuel_system_control_type": ("fuel_system_control_type_id", AcesFuelSystemControlType),
    "fuel_system_design": ("fuel_system_design_id", AcesFuelSystemDesign),
    "ignition_system_type": ("ignition_system_type_id", AcesIgnitionSystemType),

    # --- Powertrain ---
    "aspiration": ("aspiration_id", AcesAspiration),
    "power_output": ("power_output_id", AcesPowerOutput),
    "valves_per_engine": ("valves_per_engine_id", AcesValvesPerEngine),

    # --- Transmission ---
    "transmission_base": ("transmission_base_id", AcesTransmissionBase),
    "transmission_type": ("transmission_type_id", AcesTransmissionType),
    "transmission_control_type": ("transmission_control_type_id", AcesTransmissionControlType),
    "transmission_num_speeds": ("transmission_num_speeds_id", AcesTransmissionNumSpeeds),
    "transmission_mfr": ("transmission_mfr_id", AcesTransmissionMfr),
    "transmission_mfr_code": ("transmission_mfr_code_id", AcesTransmissionMfrCode),
    "trans_elec_controlled": ("trans_elec_controlled_id", AcesTransElecControlled),

    # --- Equipment ---
    "equipment_base": ("equipment_base_id", AcesEquipmentBase),
    "equipment_model": ("equipment_model_id", AcesEquipmentModel),

    # --- Manufacturer / Region ---
    "mfr": ("mfr_id", AcesMfr),
    "mfr_body_code": ("mfr_body_code_id", AcesMfrBodyCode),
    "region": ("region_id", AcesRegion),
}