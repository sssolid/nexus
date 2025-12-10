"""
VCdb (Vehicle Component Database) models.

This module defines the Django models that correspond to the VCdb database schema.
These models represent vehicle information and their components according to
Auto Care Association standards.
"""
from django.db import models
from django.utils import timezone


class Abbreviation(models.Model):
    """Abbreviation model representing abbreviations used in the system."""

    abbreviation = models.CharField(max_length=3, primary_key=True, db_index=True)
    description = models.CharField(max_length=20)
    long_description = models.CharField(max_length=200)

    class Meta:
        db_table = 'autocare_vcdb.abbreviation'
        managed = False
        verbose_name = 'Abbreviation'
        verbose_name_plural = 'Abbreviations'

    def __str__(self):
        return f"{self.abbreviation}"


class Make(models.Model):
    """Make model representing vehicle manufacturers."""

    make_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    make_name = models.CharField(max_length=50, db_index=True)

    class Meta:
        db_table = 'autocare_vcdb.make'
        managed = False
        verbose_name = 'Make'
        verbose_name_plural = 'Makes'

    def __str__(self):
        return f"{self.make_name} ({self.make_id})"


class VehicleTypeGroup(models.Model):
    """VehicleTypeGroup model representing groups of vehicle types."""

    vehicle_type_group_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    vehicle_type_group_name = models.CharField(max_length=50, db_index=True)

    class Meta:
        db_table = 'autocare_vcdb.vehicle_type_group'
        managed = False
        verbose_name = 'Vehicle Type Group'
        verbose_name_plural = 'Vehicle Type Groups'

    def __str__(self):
        return f"{self.vehicle_type_group_name} ({self.vehicle_type_group_id})"


class VehicleType(models.Model):
    """VehicleType model representing types of vehicles."""

    vehicle_type_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    vehicle_type_name = models.CharField(max_length=50, db_index=True)
    vehicle_type_group = models.ForeignKey(
        VehicleTypeGroup,
        on_delete=models.PROTECT,
        db_column='vehicle_type_group_id',
        related_name='vehicle_types',
        null=True
    )

    class Meta:
        db_table = 'autocare_vcdb.vehicle_type'
        managed = False
        verbose_name = 'Vehicle Type'
        verbose_name_plural = 'Vehicle Types'

    def __str__(self):
        return f"{self.vehicle_type_name} ({self.vehicle_type_id})"


class Model(models.Model):
    """Model model representing vehicle models."""

    model_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    model_name = models.CharField(max_length=100, db_index=True)
    vehicle_type = models.ForeignKey(
        VehicleType,
        on_delete=models.PROTECT,
        db_column='vehicle_type_id',
        related_name='models',
        db_index=True
    )

    class Meta:
        db_table = 'autocare_vcdb.model'
        managed = False
        verbose_name = 'Model'
        verbose_name_plural = 'Models'

    def __str__(self):
        return f"{self.model_name} ({self.model_id})"


class SubModel(models.Model):
    """SubModel model representing vehicle sub_models."""

    sub_model_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    sub_model_name = models.CharField(max_length=50, db_index=True)

    class Meta:
        db_table = 'autocare_vcdb.sub_model'
        managed = False
        verbose_name = 'Sub Model'
        verbose_name_plural = 'Sub Models'

    def __str__(self):
        return f"{self.sub_model_name} ({self.sub_model_id})"


class Region(models.Model):
    """Region model representing geographical regions."""

    region_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        db_column='parent_id',
        related_name='children',
        null=True
    )
    region_abbr = models.CharField(max_length=3, null=True)
    region_name = models.CharField(max_length=30, db_index=True)

    class Meta:
        db_table = 'autocare_vcdb.region'
        managed = False
        verbose_name = 'Region'
        verbose_name_plural = 'Regions'
        constraints = [
            models.UniqueConstraint(fields=['region_id'], name='uq_region_id')
        ]

    def __str__(self):
        return f"{self.region_name} ({self.region_id})"


class Year(models.Model):
    """Year model representing vehicle production years."""

    year_id = models.IntegerField(primary_key=True, unique=True, db_index=True)

    class Meta:
        db_table = 'autocare_vcdb.year'
        managed = False
        verbose_name = 'Year'
        verbose_name_plural = 'Years'

    def __str__(self):
        return f"{self.year_id}"


class PublicationStage(models.Model):
    """PublicationStage model representing stages of publication."""

    publication_stage_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    publication_stage_name = models.CharField(max_length=100, db_index=True)

    class Meta:
        db_table = 'autocare_vcdb.publication_stage'
        managed = False
        verbose_name = 'Publication Stage'
        verbose_name_plural = 'Publication Stages'

    def __str__(self):
        return f"{self.publication_stage_name} ({self.publication_stage_id})"


class BaseVehicle(models.Model):
    """BaseVehicle model representing base vehicle configurations."""

    base_vehicle_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    year = models.ForeignKey(
        Year,
        on_delete=models.PROTECT,
        db_column='year_id',
        related_name='base_vehicles',
        db_index=True
    )
    make = models.ForeignKey(
        Make,
        on_delete=models.PROTECT,
        db_column='make_id',
        related_name='base_vehicles',
        db_index=True
    )
    model = models.ForeignKey(
        Model,
        on_delete=models.PROTECT,
        db_column='model_id',
        related_name='base_vehicles',
        db_index=True
    )

    class Meta:
        db_table = 'autocare_vcdb.base_vehicle'
        managed = False
        verbose_name = 'Base Vehicle'
        verbose_name_plural = 'Base Vehicles'

    def __str__(self):
        return f"BaseVehicle {self.base_vehicle_id}"


class DriveType(models.Model):
    """DriveType model representing types of drive systems."""

    drive_type_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    drive_type_name = models.CharField(max_length=30, db_index=True)

    class Meta:
        db_table = 'autocare_vcdb.drive_type'
        managed = False
        verbose_name = 'Drive Type'
        verbose_name_plural = 'Drive Types'

    def __str__(self):
        return f"{self.drive_type_name} ({self.drive_type_id})"


class BrakeType(models.Model):
    """BrakeType model representing types of brake systems."""

    brake_type_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    brake_type_name = models.CharField(max_length=30, db_index=True)

    class Meta:
        db_table = 'autocare_vcdb.brake_type'
        managed = False
        verbose_name = 'Brake Type'
        verbose_name_plural = 'Brake Types'

    def __str__(self):
        return f"{self.brake_type_name} ({self.brake_type_id})"


class BrakeSystem(models.Model):
    """BrakeSystem model representing brake system configurations."""

    brake_system_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    brake_system_name = models.CharField(max_length=30, db_index=True)

    class Meta:
        db_table = 'autocare_vcdb.brake_system'
        managed = False
        verbose_name = 'Brake System'
        verbose_name_plural = 'Brake Systems'

    def __str__(self):
        return f"{self.brake_system_name} ({self.brake_system_id})"


class BrakeABS(models.Model):
    """BrakeABS model representing anti-lock brake systems."""

    brake_abs_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    brake_abs_name = models.CharField(max_length=30, db_index=True)

    class Meta:
        db_table = 'autocare_vcdb.brake_abs'
        managed = False
        verbose_name = 'Brake ABS'
        verbose_name_plural = 'Brake ABS'

    def __str__(self):
        return f"{self.brake_abs_name} ({self.brake_abs_id})"


class BrakeConfig(models.Model):
    """BrakeConfig model representing complete brake system configurations."""

    brake_config_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    front_brake_type = models.ForeignKey(
        BrakeType,
        on_delete=models.PROTECT,
        db_column='front_brake_type_id',
        related_name='front_brake_configs',
        db_index=True
    )
    rear_brake_type = models.ForeignKey(
        BrakeType,
        on_delete=models.PROTECT,
        db_column='rear_brake_type_id',
        related_name='rear_brake_configs',
        db_index=True
    )
    brake_system = models.ForeignKey(
        BrakeSystem,
        on_delete=models.PROTECT,
        db_column='brake_system_id',
        related_name='brake_configs',
        db_index=True
    )
    brake_abs = models.ForeignKey(
        BrakeABS,
        on_delete=models.PROTECT,
        db_column='brake_abs_id',
        related_name='brake_configs',
        db_index=True
    )

    class Meta:
        db_table = 'autocare_vcdb.brake_config'
        managed = False
        verbose_name = 'Brake Config'
        verbose_name_plural = 'Brake Configs'

    def __str__(self):
        return f"BrakeConfig {self.brake_config_id}"


class BedType(models.Model):
    """BedType model representing types of vehicle beds."""

    bed_type_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    bed_type_name = models.CharField(max_length=50, db_index=True)

    class Meta:
        db_table = 'autocare_vcdb.bed_type'
        managed = False
        verbose_name = 'Bed Type'
        verbose_name_plural = 'Bed Types'

    def __str__(self):
        return f"{self.bed_type_name} ({self.bed_type_id})"


class BedLength(models.Model):
    """BedLength model representing lengths of vehicle beds."""

    bed_length_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    bed_length = models.CharField(max_length=10)
    bed_length_metric = models.CharField(max_length=10)

    class Meta:
        db_table = 'autocare_vcdb.bed_length'
        managed = False
        verbose_name = 'Bed Length'
        verbose_name_plural = 'Bed Lengths'

    def __str__(self):
        return f"{self.bed_length} ({self.bed_length_id})"


class BedConfig(models.Model):
    """BedConfig model representing complete bed configurations."""

    bed_config_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    bed_length = models.ForeignKey(
        BedLength,
        on_delete=models.PROTECT,
        db_column='bed_length_id',
        related_name='bed_configs',
        db_index=True
    )
    bed_type = models.ForeignKey(
        BedType,
        on_delete=models.PROTECT,
        db_column='bed_type_id',
        related_name='bed_configs',
        db_index=True
    )

    class Meta:
        db_table = 'autocare_vcdb.bed_config'
        managed = False
        verbose_name = 'Bed Config'
        verbose_name_plural = 'Bed Configs'

    def __str__(self):
        return f"BedConfig {self.bed_config_id}"


class BodyType(models.Model):
    """BodyType model representing types of vehicle bodies."""

    body_type_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    body_type_name = models.CharField(max_length=50, db_index=True)

    class Meta:
        db_table = 'autocare_vcdb.body_type'
        managed = False
        verbose_name = 'Body Type'
        verbose_name_plural = 'Body Types'

    def __str__(self):
        return f"{self.body_type_name} ({self.body_type_id})"


class BodyNumDoors(models.Model):
    """BodyNumDoors model representing number of doors on vehicle bodies."""

    body_num_doors_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    body_num_doors = models.CharField(max_length=3)

    class Meta:
        db_table = 'autocare_vcdb.body_num_doors'
        managed = False
        verbose_name = 'Body Number of Doors'
        verbose_name_plural = 'Body Number of Doors'

    def __str__(self):
        return f"{self.body_num_doors} ({self.body_num_doors_id})"


class BodyStyleConfig(models.Model):
    """BodyStyleConfig model representing complete body style configurations."""

    body_style_config_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    body_num_doors = models.ForeignKey(
        BodyNumDoors,
        on_delete=models.PROTECT,
        db_column='body_num_doors_id',
        related_name='body_style_configs',
        db_index=True
    )
    body_type = models.ForeignKey(
        BodyType,
        on_delete=models.PROTECT,
        db_column='body_type_id',
        related_name='body_style_configs',
        db_index=True
    )

    class Meta:
        db_table = 'autocare_vcdb.body_style_config'
        managed = False
        verbose_name = 'Body Style Config'
        verbose_name_plural = 'Body Style Configs'

    def __str__(self):
        return f"BodyStyleConfig {self.body_style_config_id}"


class MfrBodyCode(models.Model):
    """MfrBodyCode model representing manufacturer-specific body codes."""

    mfr_body_code_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    mfr_body_code_name = models.CharField(max_length=10, db_index=True)

    class Meta:
        db_table = 'autocare_vcdb.mfr_body_code'
        managed = False
        verbose_name = 'Manufacturer Body Code'
        verbose_name_plural = 'Manufacturer Body Codes'

    def __str__(self):
        return f"{self.mfr_body_code_name} ({self.mfr_body_code_id})"


class EngineBlock(models.Model):
    """EngineBlock model representing engine block specifications."""

    engine_block_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    liter = models.CharField(max_length=6)
    cc = models.CharField(max_length=8)
    cid = models.CharField(max_length=7)
    cylinders = models.CharField(max_length=2)
    block_type = models.CharField(max_length=2)

    class Meta:
        db_table = 'autocare_vcdb.engine_block'
        managed = False
        verbose_name = 'Engine Block'
        verbose_name_plural = 'Engine Blocks'

    def __str__(self):
        return f"{self.liter}L {self.cylinders}cyl ({self.engine_block_id})"


class EngineBoreStroke(models.Model):
    """EngineBoreStroke model representing engine bore and stroke specifications."""

    engine_bore_stroke_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    eng_bore_in = models.CharField(max_length=10)
    eng_bore_metric = models.CharField(max_length=10)
    eng_stroke_in = models.CharField(max_length=10)
    eng_stroke_metric = models.CharField(max_length=10)

    class Meta:
        db_table = 'autocare_vcdb.engine_bore_stroke'
        managed = False
        verbose_name = 'Engine Bore Stroke'
        verbose_name_plural = 'Engine Bore Strokes'

    def __str__(self):
        return f"{self.eng_bore_in}x{self.eng_stroke_in} ({self.engine_bore_stroke_id})"


class EngineBase(models.Model):
    """EngineBase model representing base engine specifications for ACES 3."""

    engine_base_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    liter = models.CharField(max_length=6)
    cc = models.CharField(max_length=8)
    cid = models.CharField(max_length=7)
    cylinders = models.CharField(max_length=2)
    block_type = models.CharField(max_length=2)
    eng_bore_in = models.CharField(max_length=10)
    eng_bore_metric = models.CharField(max_length=10)
    eng_stroke_in = models.CharField(max_length=10)
    eng_stroke_metric = models.CharField(max_length=10)

    class Meta:
        db_table = 'autocare_vcdb.engine_base'
        managed = False
        verbose_name = 'Engine Base'
        verbose_name_plural = 'Engine Bases'

    def __str__(self):
        return f"EngineBase {self.engine_base_id}"


class EngineBase2(models.Model):
    """EngineBase2 model representing base engine specifications for ACES 4."""

    engine_base_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    engine_block = models.ForeignKey(
        EngineBlock,
        on_delete=models.PROTECT,
        db_column='engine_block_id',
        related_name='engine_bases',
        db_index=True
    )
    engine_bore_stroke = models.ForeignKey(
        EngineBoreStroke,
        on_delete=models.PROTECT,
        db_column='engine_bore_stroke_id',
        related_name='engine_bases',
        db_index=True
    )

    class Meta:
        db_table = 'autocare_vcdb.engine_base2'
        managed = False
        verbose_name = 'Engine Base 2'
        verbose_name_plural = 'Engine Bases 2'

    def __str__(self):
        return f"EngineBase2 {self.engine_base_id}"


class Aspiration(models.Model):
    """Aspiration model representing engine aspiration methods."""

    aspiration_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    aspiration_name = models.CharField(max_length=30, db_index=True)

    class Meta:
        db_table = 'autocare_vcdb.aspiration'
        managed = False
        verbose_name = 'Aspiration'
        verbose_name_plural = 'Aspirations'

    def __str__(self):
        return f"{self.aspiration_name} ({self.aspiration_id})"


class FuelType(models.Model):
    """FuelType model representing types of fuel used in engines."""

    fuel_type_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    fuel_type_name = models.CharField(max_length=30, db_index=True)

    class Meta:
        db_table = 'autocare_vcdb.fuel_type'
        managed = False
        verbose_name = 'Fuel Type'
        verbose_name_plural = 'Fuel Types'

    def __str__(self):
        return f"{self.fuel_type_name} ({self.fuel_type_id})"


class CylinderHeadType(models.Model):
    """CylinderHeadType model representing types of cylinder heads in engines."""

    cylinder_head_type_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    cylinder_head_type_name = models.CharField(max_length=30, db_index=True)

    class Meta:
        db_table = 'autocare_vcdb.cylinder_head_type'
        managed = False
        verbose_name = 'Cylinder Head Type'
        verbose_name_plural = 'Cylinder Head Types'

    def __str__(self):
        return f"{self.cylinder_head_type_name} ({self.cylinder_head_type_id})"


class EngineDesignation(models.Model):
    """EngineDesignation model representing engine designation specifications."""

    engine_designation_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    engine_designation_name = models.CharField(max_length=30, db_index=True)

    class Meta:
        db_table = 'autocare_vcdb.engine_designation'
        managed = False
        verbose_name = 'Engine Designation'
        verbose_name_plural = 'Engine Designations'

    def __str__(self):
        return f"{self.engine_designation_name} ({self.engine_designation_id})"


class EngineVIN(models.Model):
    """EngineVIN model representing engine VIN codes."""

    engine_vin_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    engine_vin_name = models.CharField(max_length=5, db_index=True)

    class Meta:
        db_table = 'autocare_vcdb.engine_vin'
        managed = False
        verbose_name = 'Engine VIN'
        verbose_name_plural = 'Engine VINs'

    def __str__(self):
        return f"{self.engine_vin_name} ({self.engine_vin_id})"


class EngineVersion(models.Model):
    """EngineVersion model representing engine version specifications."""

    engine_version_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    engine_version = models.CharField(max_length=20, db_index=True)

    class Meta:
        db_table = 'autocare_vcdb.engine_version'
        managed = False
        verbose_name = 'Engine Version'
        verbose_name_plural = 'Engine Versions'

    def __str__(self):
        return f"{self.engine_version} ({self.engine_version_id})"


class Valves(models.Model):
    """Valves model representing engine valve configurations."""

    valves_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    valves_per_engine = models.CharField(max_length=3)

    class Meta:
        db_table = 'autocare_vcdb.valves'
        managed = False
        verbose_name = 'Valves'
        verbose_name_plural = 'Valves'

    def __str__(self):
        return f"{self.valves_per_engine} ({self.valves_id})"


class FuelDeliveryType(models.Model):
    """FuelDeliveryType model representing types of fuel delivery systems."""

    fuel_delivery_type_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    fuel_delivery_type_name = models.CharField(max_length=50, db_index=True)

    class Meta:
        db_table = 'autocare_vcdb.fuel_delivery_type'
        managed = False
        verbose_name = 'Fuel Delivery Type'
        verbose_name_plural = 'Fuel Delivery Types'

    def __str__(self):
        return f"{self.fuel_delivery_type_name} ({self.fuel_delivery_type_id})"


class FuelDeliverySubType(models.Model):
    """FuelDeliverySubType model representing subtypes of fuel delivery systems."""

    fuel_delivery_sub_type_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    fuel_delivery_sub_type_name = models.CharField(max_length=50, db_index=True)

    class Meta:
        db_table = 'autocare_vcdb.fuel_delivery_sub_type'
        managed = False
        verbose_name = 'Fuel Delivery Sub Type'
        verbose_name_plural = 'Fuel Delivery Sub Types'

    def __str__(self):
        return f"{self.fuel_delivery_sub_type_name} ({self.fuel_delivery_sub_type_id})"


class FuelSystemControlType(models.Model):
    """FuelSystemControlType model representing types of fuel system control mechanisms."""

    fuel_system_control_type_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    fuel_system_control_type_name = models.CharField(max_length=50, db_index=True)

    class Meta:
        db_table = 'autocare_vcdb.fuel_system_control_type'
        managed = False
        verbose_name = 'Fuel System Control Type'
        verbose_name_plural = 'Fuel System Control Types'

    def __str__(self):
        return f"{self.fuel_system_control_type_name} ({self.fuel_system_control_type_id})"


class FuelSystemDesign(models.Model):
    """FuelSystemDesign model representing designs of fuel systems."""

    fuel_system_design_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    fuel_system_design_name = models.CharField(max_length=50, db_index=True)

    class Meta:
        db_table = 'autocare_vcdb.fuel_system_design'
        managed = False
        verbose_name = 'Fuel System Design'
        verbose_name_plural = 'Fuel System Designs'

    def __str__(self):
        return f"{self.fuel_system_design_name} ({self.fuel_system_design_id})"


class FuelDeliveryConfig(models.Model):
    """FuelDeliveryConfig model representing complete fuel delivery system configurations."""

    fuel_delivery_config_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    fuel_delivery_type = models.ForeignKey(
        FuelDeliveryType,
        on_delete=models.PROTECT,
        db_column='fuel_delivery_type_id',
        related_name='fuel_delivery_configs',
        db_index=True
    )
    fuel_delivery_sub_type = models.ForeignKey(
        FuelDeliverySubType,
        on_delete=models.PROTECT,
        db_column='fuel_delivery_sub_type_id',
        related_name='fuel_delivery_configs',
        db_index=True
    )
    fuel_system_control_type = models.ForeignKey(
        FuelSystemControlType,
        on_delete=models.PROTECT,
        db_column='fuel_system_control_type_id',
        related_name='fuel_delivery_configs',
        db_index=True
    )
    fuel_system_design = models.ForeignKey(
        FuelSystemDesign,
        on_delete=models.PROTECT,
        db_column='fuel_system_design_id',
        related_name='fuel_delivery_configs',
        db_index=True
    )

    class Meta:
        db_table = 'autocare_vcdb.fuel_delivery_config'
        managed = False
        verbose_name = 'Fuel Delivery Config'
        verbose_name_plural = 'Fuel Delivery Configs'

    def __str__(self):
        return f"FuelDeliveryConfig {self.fuel_delivery_config_id}"


class PowerOutput(models.Model):
    """PowerOutput model representing engine power output specifications."""

    power_output_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    horse_power = models.CharField(max_length=10)
    kilowatt_power = models.CharField(max_length=10)

    class Meta:
        db_table = 'autocare_vcdb.power_output'
        managed = False
        verbose_name = 'Power Output'
        verbose_name_plural = 'Power Outputs'

    def __str__(self):
        return f"{self.horse_power}hp/{self.kilowatt_power}kw ({self.power_output_id})"


class Mfr(models.Model):
    """Mfr model representing manufacturers."""

    mfr_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    mfr_name = models.CharField(max_length=30, db_index=True)

    class Meta:
        db_table = 'autocare_vcdb.mfr'
        managed = False
        verbose_name = 'Manufacturer'
        verbose_name_plural = 'Manufacturers'

    def __str__(self):
        return f"{self.mfr_name} ({self.mfr_id})"


class IgnitionSystemType(models.Model):
    """IgnitionSystemType model representing types of ignition systems."""

    ignition_system_type_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    ignition_system_type_name = models.CharField(max_length=30, db_index=True)

    class Meta:
        db_table = 'autocare_vcdb.ignition_system_type'
        managed = False
        verbose_name = 'Ignition System Type'
        verbose_name_plural = 'Ignition System Types'

    def __str__(self):
        return f"{self.ignition_system_type_name} ({self.ignition_system_type_id})"


class EngineConfig(models.Model):
    """EngineConfig model representing complete engine configurations for ACES 3."""

    engine_config_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    engine_base = models.ForeignKey(
        EngineBase,
        on_delete=models.PROTECT,
        db_column='engine_base_id',
        related_name='engine_configs',
        db_index=True
    )
    engine_designation = models.ForeignKey(
        EngineDesignation,
        on_delete=models.PROTECT,
        db_column='engine_designation_id',
        related_name='engine_configs',
        db_index=True
    )
    engine_vin = models.ForeignKey(
        EngineVIN,
        on_delete=models.PROTECT,
        db_column='engine_vin_id',
        related_name='engine_configs',
        db_index=True
    )
    valves = models.ForeignKey(
        Valves,
        on_delete=models.PROTECT,
        db_column='valves_id',
        related_name='engine_configs',
        db_index=True
    )
    fuel_delivery_config = models.ForeignKey(
        FuelDeliveryConfig,
        on_delete=models.PROTECT,
        db_column='fuel_delivery_config_id',
        related_name='engine_configs',
        db_index=True
    )
    aspiration = models.ForeignKey(
        Aspiration,
        on_delete=models.PROTECT,
        db_column='aspiration_id',
        related_name='engine_configs',
        db_index=True
    )
    cylinder_head_type = models.ForeignKey(
        CylinderHeadType,
        on_delete=models.PROTECT,
        db_column='cylinder_head_type_id',
        related_name='engine_configs',
        db_index=True
    )
    fuel_type = models.ForeignKey(
        FuelType,
        on_delete=models.PROTECT,
        db_column='fuel_type_id',
        related_name='engine_configs',
        db_index=True
    )
    ignition_system_type = models.ForeignKey(
        IgnitionSystemType,
        on_delete=models.PROTECT,
        db_column='ignition_system_type_id',
        related_name='engine_configs',
        db_index=True
    )
    engine_mfr = models.ForeignKey(
        Mfr,
        on_delete=models.PROTECT,
        db_column='engine_mfr_id',
        related_name='engine_configs',
        db_index=True
    )
    engine_version = models.ForeignKey(
        EngineVersion,
        on_delete=models.PROTECT,
        db_column='engine_version_id',
        related_name='engine_configs',
        db_index=True
    )
    power_output = models.ForeignKey(
        PowerOutput,
        on_delete=models.PROTECT,
        db_column='power_output_id',
        related_name='engine_configs',
        db_index=True,
        default=1
    )

    class Meta:
        db_table = 'autocare_vcdb.engine_config'
        managed = False
        verbose_name = 'Engine Config'
        verbose_name_plural = 'Engine Configs'

    def __str__(self):
        return f"EngineConfig {self.engine_config_id}"


class EngineConfig2(models.Model):
    """EngineConfig2 model representing complete engine configurations for ACES 4."""

    engine_config_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    engine_base = models.ForeignKey(
        EngineBase2,
        on_delete=models.PROTECT,
        db_column='engine_base_id',
        related_name='engine_configs',
        db_index=True
    )
    engine_block = models.ForeignKey(
        EngineBlock,
        on_delete=models.PROTECT,
        db_column='engine_block_id',
        related_name='engine_configs',
        db_index=True
    )
    engine_bore_stroke = models.ForeignKey(
        EngineBoreStroke,
        on_delete=models.PROTECT,
        db_column='engine_bore_stroke_id',
        related_name='engine_configs',
        db_index=True
    )
    engine_designation = models.ForeignKey(
        EngineDesignation,
        on_delete=models.PROTECT,
        db_column='engine_designation_id',
        related_name='engine_configs2',
        db_index=True
    )
    engine_vin = models.ForeignKey(
        EngineVIN,
        on_delete=models.PROTECT,
        db_column='engine_vin_id',
        related_name='engine_configs2',
        db_index=True
    )
    valves = models.ForeignKey(
        Valves,
        on_delete=models.PROTECT,
        db_column='valves_id',
        related_name='engine_configs2',
        db_index=True
    )
    fuel_delivery_config = models.ForeignKey(
        FuelDeliveryConfig,
        on_delete=models.PROTECT,
        db_column='fuel_delivery_config_id',
        related_name='engine_configs2',
        db_index=True
    )
    aspiration = models.ForeignKey(
        Aspiration,
        on_delete=models.PROTECT,
        db_column='aspiration_id',
        related_name='engine_configs2',
        db_index=True
    )
    cylinder_head_type = models.ForeignKey(
        CylinderHeadType,
        on_delete=models.PROTECT,
        db_column='cylinder_head_type_id',
        related_name='engine_configs2',
        db_index=True
    )
    fuel_type = models.ForeignKey(
        FuelType,
        on_delete=models.PROTECT,
        db_column='fuel_type_id',
        related_name='engine_configs2',
        db_index=True
    )
    ignition_system_type = models.ForeignKey(
        IgnitionSystemType,
        on_delete=models.PROTECT,
        db_column='ignition_system_type_id',
        related_name='engine_configs2',
        db_index=True
    )
    engine_mfr = models.ForeignKey(
        Mfr,
        on_delete=models.PROTECT,
        db_column='engine_mfr_id',
        related_name='engine_configs2',
        db_index=True
    )
    engine_version = models.ForeignKey(
        EngineVersion,
        on_delete=models.PROTECT,
        db_column='engine_version_id',
        related_name='engine_configs2',
        db_index=True
    )
    power_output = models.ForeignKey(
        PowerOutput,
        on_delete=models.PROTECT,
        db_column='power_output_id',
        related_name='engine_configs2',
        db_index=True,
        default=1
    )

    class Meta:
        db_table = 'autocare_vcdb.engine_config2'
        managed = False
        verbose_name = 'Engine Config 2'
        verbose_name_plural = 'Engine Configs 2'

    def __str__(self):
        return f"EngineConfig2 {self.engine_config_id}"


class SpringType(models.Model):
    """SpringType model representing types of vehicle springs."""

    spring_type_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    spring_type_name = models.CharField(max_length=50, db_index=True)

    class Meta:
        db_table = 'autocare_vcdb.spring_type'
        managed = False
        verbose_name = 'Spring Type'
        verbose_name_plural = 'Spring Types'

    def __str__(self):
        return f"{self.spring_type_name} ({self.spring_type_id})"


class SpringTypeConfig(models.Model):
    """SpringTypeConfig model representing complete spring type configurations."""

    spring_type_config_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    front_spring_type = models.ForeignKey(
        SpringType,
        on_delete=models.PROTECT,
        db_column='front_spring_type_id',
        related_name='front_spring_configs',
        db_index=True
    )
    rear_spring_type = models.ForeignKey(
        SpringType,
        on_delete=models.PROTECT,
        db_column='rear_spring_type_id',
        related_name='rear_spring_configs',
        db_index=True
    )

    class Meta:
        db_table = 'autocare_vcdb.spring_type_config'
        managed = False
        verbose_name = 'Spring Type Config'
        verbose_name_plural = 'Spring Type Configs'

    def __str__(self):
        return f"SpringTypeConfig {self.spring_type_config_id}"


class SteeringType(models.Model):
    """SteeringType model representing types of steering systems."""

    steering_type_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    steering_type_name = models.CharField(max_length=30, db_index=True)

    class Meta:
        db_table = 'autocare_vcdb.steering_type'
        managed = False
        verbose_name = 'Steering Type'
        verbose_name_plural = 'Steering Types'

    def __str__(self):
        return f"{self.steering_type_name} ({self.steering_type_id})"


class SteeringSystem(models.Model):
    """SteeringSystem model representing steering system configurations."""

    steering_system_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    steering_system_name = models.CharField(max_length=30, db_index=True)

    class Meta:
        db_table = 'autocare_vcdb.steering_system'
        managed = False
        verbose_name = 'Steering System'
        verbose_name_plural = 'Steering Systems'

    def __str__(self):
        return f"{self.steering_system_name} ({self.steering_system_id})"


class SteeringConfig(models.Model):
    """SteeringConfig model representing complete steering configurations."""

    steering_config_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    steering_type = models.ForeignKey(
        SteeringType,
        on_delete=models.PROTECT,
        db_column='steering_type_id',
        related_name='steering_configs',
        db_index=True
    )
    steering_system = models.ForeignKey(
        SteeringSystem,
        on_delete=models.PROTECT,
        db_column='steering_system_id',
        related_name='steering_configs',
        db_index=True
    )

    class Meta:
        db_table = 'autocare_vcdb.steering_config'
        managed = False
        verbose_name = 'Steering Config'
        verbose_name_plural = 'Steering Configs'

    def __str__(self):
        return f"SteeringConfig {self.steering_config_id}"


class TransmissionType(models.Model):
    """TransmissionType model representing types of transmissions."""

    transmission_type_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    transmission_type_name = models.CharField(max_length=30, db_index=True)

    class Meta:
        db_table = 'autocare_vcdb.transmission_type'
        managed = False
        verbose_name = 'Transmission Type'
        verbose_name_plural = 'Transmission Types'

    def __str__(self):
        return f"{self.transmission_type_name} ({self.transmission_type_id})"


class TransmissionNumSpeeds(models.Model):
    """TransmissionNumSpeeds model representing number of speeds in transmissions."""

    transmission_num_speeds_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    transmission_num_speeds = models.CharField(max_length=3, db_index=True)

    class Meta:
        db_table = 'autocare_vcdb.transmission_num_speeds'
        managed = False
        verbose_name = 'Transmission Number of Speeds'
        verbose_name_plural = 'Transmission Number of Speeds'

    def __str__(self):
        return f"{self.transmission_num_speeds} ({self.transmission_num_speeds_id})"


class TransmissionControlType(models.Model):
    """TransmissionControlType model representing types of transmission control systems."""

    transmission_control_type_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    transmission_control_type_name = models.CharField(max_length=30, db_index=True)

    class Meta:
        db_table = 'autocare_vcdb.transmission_control_type'
        managed = False
        verbose_name = 'Transmission Control Type'
        verbose_name_plural = 'Transmission Control Types'

    def __str__(self):
        return f"{self.transmission_control_type_name} ({self.transmission_control_type_id})"


class TransmissionBase(models.Model):
    """TransmissionBase model representing base transmission configurations."""

    transmission_base_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    transmission_type = models.ForeignKey(
        TransmissionType,
        on_delete=models.PROTECT,
        db_column='transmission_type_id',
        related_name='transmission_bases',
        db_index=True
    )
    transmission_num_speeds = models.ForeignKey(
        TransmissionNumSpeeds,
        on_delete=models.PROTECT,
        db_column='transmission_num_speeds_id',
        related_name='transmission_bases',
        db_index=True
    )
    transmission_control_type = models.ForeignKey(
        TransmissionControlType,
        on_delete=models.PROTECT,
        db_column='transmission_control_type_id',
        related_name='transmission_bases',
        db_index=True
    )

    class Meta:
        db_table = 'autocare_vcdb.transmission_base'
        managed = False
        verbose_name = 'Transmission Base'
        verbose_name_plural = 'Transmission Bases'

    def __str__(self):
        return f"TransmissionBase {self.transmission_base_id}"


class TransmissionMfrCode(models.Model):
    """TransmissionMfrCode model representing manufacturer codes for transmissions."""

    transmission_mfr_code_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    transmission_mfr_code = models.CharField(max_length=30, db_index=True)

    class Meta:
        db_table = 'autocare_vcdb.transmission_mfr_code'
        managed = False
        verbose_name = 'Transmission Manufacturer Code'
        verbose_name_plural = 'Transmission Manufacturer Codes'

    def __str__(self):
        return f"{self.transmission_mfr_code} ({self.transmission_mfr_code_id})"


class ElecControlled(models.Model):
    """ElecControlled model representing electrically controlled components."""

    elec_controlled_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    elec_controlled = models.CharField(max_length=3, db_index=True)

    class Meta:
        db_table = 'autocare_vcdb.elec_controlled'
        managed = False
        verbose_name = 'Electrically Controlled'
        verbose_name_plural = 'Electrically Controlled'

    def __str__(self):
        return f"{self.elec_controlled} ({self.elec_controlled_id})"


class Transmission(models.Model):
    """Transmission model representing complete transmission configurations."""

    transmission_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    transmission_base = models.ForeignKey(
        TransmissionBase,
        on_delete=models.PROTECT,
        db_column='transmission_base_id',
        related_name='transmissions',
        db_index=True
    )
    transmission_mfr_code = models.ForeignKey(
        TransmissionMfrCode,
        on_delete=models.PROTECT,
        db_column='transmission_mfr_code_id',
        related_name='transmissions',
        db_index=True
    )
    elec_controlled = models.ForeignKey(
        ElecControlled,
        on_delete=models.PROTECT,
        db_column='transmission_elec_controlled_id',
        related_name='transmissions',
        db_index=True
    )
    transmission_mfr = models.ForeignKey(
        Mfr,
        on_delete=models.PROTECT,
        db_column='transmission_mfr_id',
        related_name='transmission_configs',
        db_index=True
    )

    class Meta:
        db_table = 'autocare_vcdb.transmission'
        managed = False
        verbose_name = 'Transmission'
        verbose_name_plural = 'Transmissions'

    def __str__(self):
        return f"Transmission {self.transmission_id}"


class WheelBase(models.Model):
    """WheelBase model representing wheel base specifications."""

    wheel_base_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    wheel_base = models.CharField(max_length=10)
    wheel_base_metric = models.CharField(max_length=10)

    class Meta:
        db_table = 'autocare_vcdb.wheel_base'
        managed = False
        verbose_name = 'Wheel Base'
        verbose_name_plural = 'Wheel Bases'

    def __str__(self):
        return f"{self.wheel_base} ({self.wheel_base_id})"


class VehicleClass(models.Model):
    """Class model representing vehicle classifications."""

    class_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    class_name = models.CharField(max_length=30, db_index=True)

    class Meta:
        db_table = 'autocare_vcdb.class'
        managed = False
        verbose_name = 'Vehicle Class'
        verbose_name_plural = 'Vehicle Classes'

    def __str__(self):
        return f"{self.class_name} ({self.class_id})"


class Vehicle(models.Model):
    """Vehicle model representing specific vehicle configurations."""

    vehicle_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    base_vehicle = models.ForeignKey(
        BaseVehicle,
        on_delete=models.PROTECT,
        db_column='base_vehicle_id',
        related_name='vehicles',
        db_index=True
    )
    sub_model = models.ForeignKey(
        SubModel,
        on_delete=models.PROTECT,
        db_column='sub_model_id',
        related_name='vehicles',
        db_index=True
    )
    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        db_column='region_id',
        related_name='vehicles',
        db_index=True
    )
    source = models.CharField(max_length=10, null=True)
    publication_stage = models.ForeignKey(
        PublicationStage,
        on_delete=models.PROTECT,
        db_column='publication_stage_id',
        related_name='vehicles',
        db_index=True,
        default=4
    )
    publication_stage_source = models.CharField(max_length=100)
    publication_stage_date = models.DateTimeField(default=timezone.now)

    # Many-to-many relationships through junction tables
    drive_types = models.ManyToManyField(
        DriveType,
        through='VehicleToDriveType',
        related_name='vehicles'
    )
    brake_configs = models.ManyToManyField(
        BrakeConfig,
        through='VehicleToBrakeConfig',
        related_name='vehicles'
    )
    bed_configs = models.ManyToManyField(
        BedConfig,
        through='VehicleToBedConfig',
        related_name='vehicles'
    )
    body_style_configs = models.ManyToManyField(
        BodyStyleConfig,
        through='VehicleToBodyStyleConfig',
        related_name='vehicles'
    )
    mfr_body_codes = models.ManyToManyField(
        MfrBodyCode,
        through='VehicleToMfrBodyCode',
        related_name='vehicles'
    )
    engine_configs = models.ManyToManyField(
        EngineConfig2,
        through='VehicleToEngineConfig',
        related_name='vehicles'
    )
    spring_type_configs = models.ManyToManyField(
        SpringTypeConfig,
        through='VehicleToSpringTypeConfig',
        related_name='vehicles'
    )
    steering_configs = models.ManyToManyField(
        SteeringConfig,
        through='VehicleToSteeringConfig',
        related_name='vehicles'
    )
    transmissions = models.ManyToManyField(
        Transmission,
        through='VehicleToTransmission',
        related_name='vehicles'
    )
    wheel_bases = models.ManyToManyField(
        WheelBase,
        through='VehicleToWheelBase',
        related_name='vehicles'
    )
    classes = models.ManyToManyField(
        VehicleClass,
        through='VehicleToClass',
        related_name='vehicles'
    )

    class Meta:
        db_table = 'autocare_vcdb.vehicle'
        managed = False
        verbose_name = 'Vehicle'
        verbose_name_plural = 'Vehicles'

    def __str__(self):
        return f"Vehicle {self.vehicle_id}"

    @property
    def make(self):
        """Get the make of the vehicle."""
        return self.base_vehicle.make

    @property
    def year(self):
        """Get the year of the vehicle."""
        if self.base_vehicle and self.base_vehicle.year:
            return self.base_vehicle.year.year_id
        return None

    @property
    def model(self):
        """Get the model name of the vehicle."""
        return self.base_vehicle.model.model_name


# Junction table models
class VehicleToDriveType(models.Model):
    """VehicleToDriveType model representing the relationship between vehicles and drive types."""

    vehicle_to_drive_type_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        db_column='vehicle_id',
        db_index=True
    )
    drive_type = models.ForeignKey(
        DriveType,
        on_delete=models.PROTECT,
        db_column='drive_type_id',
        db_index=True
    )
    source = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = 'autocare_vcdb.vehicle_to_drive_type'
        managed = False
        verbose_name = 'Vehicle to Drive Type'
        verbose_name_plural = 'Vehicle to Drive Types'

    def __str__(self):
        return f"VehicleToDriveType {self.vehicle_to_drive_type_id}"


class VehicleToBrakeConfig(models.Model):
    """VehicleToBrakeConfig model representing the relationship between vehicles and brake configurations."""

    vehicle_to_brake_config_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        db_column='vehicle_id',
        db_index=True
    )
    brake_config = models.ForeignKey(
        BrakeConfig,
        on_delete=models.PROTECT,
        db_column='brake_config_id',
        db_index=True
    )
    source = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = 'autocare_vcdb.vehicle_to_brake_config'
        managed = False
        verbose_name = 'Vehicle to Brake Config'
        verbose_name_plural = 'Vehicle to Brake Configs'

    def __str__(self):
        return f"VehicleToBrakeConfig {self.vehicle_to_brake_config_id}"


class VehicleToBedConfig(models.Model):
    """VehicleToBedConfig model representing the relationship between vehicles and bed configurations."""

    vehicle_to_bed_config_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        db_column='vehicle_id',
        db_index=True
    )
    bed_config = models.ForeignKey(
        BedConfig,
        on_delete=models.PROTECT,
        db_column='bed_config_id',
        db_index=True
    )
    source = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = 'autocare_vcdb.vehicle_to_bed_config'
        managed = False
        verbose_name = 'Vehicle to Bed Config'
        verbose_name_plural = 'Vehicle to Bed Configs'

    def __str__(self):
        return f"VehicleToBedConfig {self.vehicle_to_bed_config_id}"


class VehicleToBodyStyleConfig(models.Model):
    """VehicleToBodyStyleConfig model representing the relationship between vehicles and body style configurations."""

    vehicle_to_body_style_config_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        db_column='vehicle_id',
        db_index=True
    )
    body_style_config = models.ForeignKey(
        BodyStyleConfig,
        on_delete=models.PROTECT,
        db_column='body_style_config_id',
        db_index=True
    )
    source = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = 'autocare_vcdb.vehicle_to_body_style_config'
        managed = False
        verbose_name = 'Vehicle to Body Style Config'
        verbose_name_plural = 'Vehicle to Body Style Configs'

    def __str__(self):
        return f"VehicleToBodyStyleConfig {self.vehicle_to_body_style_config_id}"


class VehicleToMfrBodyCode(models.Model):
    """VehicleToMfrBodyCode model representing the relationship between vehicles and manufacturer body codes."""

    vehicle_to_mfr_body_code_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        db_column='vehicle_id',
        db_index=True
    )
    mfr_body_code = models.ForeignKey(
        MfrBodyCode,
        on_delete=models.PROTECT,
        db_column='mfr_body_code_id',
        db_index=True
    )
    source = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = 'autocare_vcdb.vehicle_to_mfr_body_code'
        managed = False
        verbose_name = 'Vehicle to Manufacturer Body Code'
        verbose_name_plural = 'Vehicle to Manufacturer Body Codes'

    def __str__(self):
        return f"VehicleToMfrBodyCode {self.vehicle_to_mfr_body_code_id}"


class VehicleToEngineConfig(models.Model):
    """VehicleToEngineConfig model representing the relationship between vehicles and engine configurations."""

    vehicle_to_engine_config_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        db_column='vehicle_id',
        db_index=True
    )
    engine_config = models.ForeignKey(
        EngineConfig2,
        on_delete=models.PROTECT,
        db_column='engine_config_id',
        db_index=True
    )
    source = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = 'autocare_vcdb.vehicle_to_engine_config'
        managed = False
        verbose_name = 'Vehicle to Engine Config'
        verbose_name_plural = 'Vehicle to Engine Configs'

    def __str__(self):
        return f"VehicleToEngineConfig {self.vehicle_to_engine_config_id}"


class VehicleToSpringTypeConfig(models.Model):
    """VehicleToSpringTypeConfig model representing the relationship between vehicles and spring type configurations."""

    vehicle_to_spring_type_config_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        db_column='vehicle_id',
        db_index=True
    )
    spring_type_config = models.ForeignKey(
        SpringTypeConfig,
        on_delete=models.PROTECT,
        db_column='spring_type_config_id',
        db_index=True
    )
    source = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = 'autocare_vcdb.vehicle_to_spring_type_config'
        managed = False
        verbose_name = 'Vehicle to Spring Type Config'
        verbose_name_plural = 'Vehicle to Spring Type Configs'

    def __str__(self):
        return f"VehicleToSpringTypeConfig {self.vehicle_to_spring_type_config_id}"


class VehicleToSteeringConfig(models.Model):
    """VehicleToSteeringConfig model representing the relationship between vehicles and steering configurations."""

    vehicle_to_steering_config_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        db_column='vehicle_id',
        db_index=True
    )
    steering_config = models.ForeignKey(
        SteeringConfig,
        on_delete=models.PROTECT,
        db_column='steering_config_id',
        db_index=True
    )
    source = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = 'autocare_vcdb.vehicle_to_steering_config'
        managed = False
        verbose_name = 'Vehicle to Steering Config'
        verbose_name_plural = 'Vehicle to Steering Configs'

    def __str__(self):
        return f"VehicleToSteeringConfig {self.vehicle_to_steering_config_id}"


class VehicleToTransmission(models.Model):
    """VehicleToTransmission model representing the relationship between vehicles and transmissions."""

    vehicle_to_transmission_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        db_column='vehicle_id',
        db_index=True
    )
    transmission = models.ForeignKey(
        Transmission,
        on_delete=models.PROTECT,
        db_column='transmission_id',
        db_index=True
    )
    source = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = 'autocare_vcdb.vehicle_to_transmission'
        managed = False
        verbose_name = 'Vehicle to Transmission'
        verbose_name_plural = 'Vehicle to Transmissions'

    def __str__(self):
        return f"VehicleToTransmission {self.vehicle_to_transmission_id}"


class VehicleToWheelBase(models.Model):
    """VehicleToWheelBase model representing the relationship between vehicles and wheel bases."""

    vehicle_to_wheel_base_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        db_column='vehicle_id',
        db_index=True
    )
    wheel_base = models.ForeignKey(
        WheelBase,
        on_delete=models.PROTECT,
        db_column='wheel_base_id',
        db_index=True
    )
    source = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = 'autocare_vcdb.vehicle_to_wheel_base'
        managed = False
        verbose_name = 'Vehicle to Wheel Base'
        verbose_name_plural = 'Vehicle to Wheel Bases'

    def __str__(self):
        return f"VehicleToWheelBase {self.vehicle_to_wheel_base_id}"


class VehicleToClass(models.Model):
    """VehicleToClass model representing the relationship between vehicles and classes."""

    vehicle_to_class_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        db_column='vehicle_id',
        db_index=True
    )
    vehicle_class = models.ForeignKey(
        VehicleClass,
        on_delete=models.PROTECT,
        db_column='class_id',
        db_index=True
    )
    source = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = 'autocare_vcdb.vehicle_to_class'
        managed = False
        verbose_name = 'Vehicle to Class'
        verbose_name_plural = 'Vehicle to Classes'

    def __str__(self):
        return f"VehicleToClass {self.vehicle_to_class_id}"


class VehicleToBodyConfig(models.Model):
    """VehicleToBodyConfig model representing the relationship between vehicles and body configurations."""

    vehicle_to_body_config_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        db_column='vehicle_id',
        related_name='body_configs',
        db_index=True
    )
    wheel_base = models.ForeignKey(
        WheelBase,
        on_delete=models.PROTECT,
        db_column='wheel_base_id',
        db_index=True
    )
    bed_config = models.ForeignKey(
        BedConfig,
        on_delete=models.PROTECT,
        db_column='bed_config_id',
        db_index=True
    )
    body_style_config = models.ForeignKey(
        BodyStyleConfig,
        on_delete=models.PROTECT,
        db_column='body_style_config_id',
        db_index=True
    )
    mfr_body_code = models.ForeignKey(
        MfrBodyCode,
        on_delete=models.PROTECT,
        db_column='mfr_body_code_id',
        db_index=True
    )
    source = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = 'autocare_vcdb.vehicle_to_body_config'
        managed = False
        verbose_name = 'Vehicle to Body Config'
        verbose_name_plural = 'Vehicle to Body Configs'

    def __str__(self):
        return f"VehicleToBodyConfig {self.vehicle_to_body_config_id}"


# Change tracking and version models
class ChangeAttributeStates(models.Model):
    """ChangeAttributeStates model representing states of attribute changes."""

    change_attribute_state_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    change_attribute_state = models.CharField(max_length=255)

    class Meta:
        db_table = 'autocare_vcdb.change_attribute_states'
        managed = False
        verbose_name = 'Change Attribute State'
        verbose_name_plural = 'Change Attribute States'

    def __str__(self):
        return f"{self.change_attribute_state} ({self.change_attribute_state_id})"


class ChangeReasons(models.Model):
    """ChangeReasons model representing reasons for changes."""

    change_reason_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    change_reason = models.CharField(max_length=255)

    class Meta:
        db_table = 'autocare_vcdb.change_reasons'
        managed = False
        verbose_name = 'Change Reason'
        verbose_name_plural = 'Change Reasons'

    def __str__(self):
        return f"{self.change_reason} ({self.change_reason_id})"


class ChangeTableNames(models.Model):
    """ChangeTableNames model representing names of tables that can be changed."""

    table_name_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    table_name = models.CharField(max_length=255)
    table_description = models.CharField(max_length=1000, null=True)

    class Meta:
        db_table = 'autocare_vcdb.change_table_names'
        managed = False
        verbose_name = 'Change Table Name'
        verbose_name_plural = 'Change Table Names'

    def __str__(self):
        return f"{self.table_name} ({self.table_name_id})"


class Changes(models.Model):
    """Changes model representing change records."""

    change_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    request_id = models.IntegerField()
    change_reason = models.ForeignKey(
        ChangeReasons,
        on_delete=models.PROTECT,
        db_column='change_reason_id',
        related_name='changes',
        db_index=True
    )
    rev_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'autocare_vcdb.changes'
        managed = False
        verbose_name = 'Change'
        verbose_name_plural = 'Changes'

    def __str__(self):
        return f"Change {self.change_id}"


class ChangeDetails(models.Model):
    """ChangeDetails model representing details of changes."""

    change_detail_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    change = models.ForeignKey(
        Changes,
        on_delete=models.CASCADE,
        db_column='change_id',
        related_name='change_details',
        db_index=True
    )
    change_attribute_state = models.ForeignKey(
        ChangeAttributeStates,
        on_delete=models.PROTECT,
        db_column='change_attribute_state_id',
        related_name='change_details',
        db_index=True
    )
    table_name = models.ForeignKey(
        ChangeTableNames,
        on_delete=models.PROTECT,
        db_column='table_name_id',
        related_name='change_details',
        db_index=True
    )
    primary_key_column_name = models.CharField(max_length=255, null=True)
    primary_key_before = models.IntegerField(null=True)
    primary_key_after = models.IntegerField(null=True)
    column_name = models.CharField(max_length=255, null=True)
    column_value_before = models.CharField(max_length=1000, null=True)
    column_value_after = models.CharField(max_length=1000, null=True)

    class Meta:
        db_table = 'autocare_vcdb.change_details'
        managed = False
        verbose_name = 'Change Detail'
        verbose_name_plural = 'Change Details'

    def __str__(self):
        return f"ChangeDetails {self.change_detail_id}"


class Version(models.Model):
    """Version model representing VCdb version information."""

    version_date = models.DateTimeField(primary_key=True, db_index=True)

    class Meta:
        db_table = 'autocare_vcdb.version'
        managed = False
        verbose_name = 'Version'
        verbose_name_plural = 'Versions'

    def __str__(self):
        return f"Version {self.version_date}"


class VCdbChanges(models.Model):
    """VCdbChanges model representing changes to the VCdb."""

    id = models.IntegerField(primary_key=True)
    version_date = models.DateTimeField()
    table_name = models.CharField(max_length=30)
    action = models.CharField(max_length=1)

    class Meta:
        db_table = 'autocare_vcdb.vcdb_changes'
        managed = False
        verbose_name = 'VCdb Change'
        verbose_name_plural = 'VCdb Changes'

    def __str__(self):
        return f"{self.table_name} {self.id} {self.action}"


# Translation and localization models
class AttachmentType(models.Model):
    """AttachmentType model representing types of attachments."""

    attachment_type_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    attachment_type_name = models.CharField(max_length=20)

    class Meta:
        db_table = 'autocare_vcdb.attachment_type'
        managed = False
        verbose_name = 'Attachment Type'
        verbose_name_plural = 'Attachment Types'

    def __str__(self):
        return f"{self.attachment_type_name} ({self.attachment_type_id})"


class Attachment(models.Model):
    """Attachment model representing file attachments."""

    attachment_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    attachment_type = models.ForeignKey(
        AttachmentType,
        on_delete=models.PROTECT,
        db_column='attachment_type_id',
        related_name='attachments',
        db_index=True
    )
    attachment_file_name = models.CharField(max_length=50)
    attachment_url = models.CharField(max_length=100)
    attachment_description = models.CharField(max_length=50)

    class Meta:
        db_table = 'autocare_vcdb.attachment'
        managed = False
        verbose_name = 'Attachment'
        verbose_name_plural = 'Attachments'

    def __str__(self):
        return f"{self.attachment_file_name} ({self.attachment_id})"


class EnglishPhrase(models.Model):
    """EnglishPhrase model representing English phrases for translation."""

    english_phrase_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    english_phrase = models.CharField(max_length=100)

    class Meta:
        db_table = 'autocare_vcdb.english_phrase'
        managed = False
        verbose_name = 'English Phrase'
        verbose_name_plural = 'English Phrases'

    def __str__(self):
        return f"{self.english_phrase} ({self.english_phrase_id})"


class Language(models.Model):
    """Language model representing languages for translation."""

    language_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    language_name = models.CharField(max_length=20)
    dialect_name = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = 'autocare_vcdb.language'
        managed = False
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'

    def __str__(self):
        return f"{self.language_name} ({self.language_id})"


class LanguageTranslation(models.Model):
    """LanguageTranslation model representing translations of phrases into different languages."""

    language_translation_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    english_phrase = models.ForeignKey(
        EnglishPhrase,
        on_delete=models.CASCADE,
        db_column='english_phrase_id',
        related_name='language_translations',
        db_index=True
    )
    language = models.ForeignKey(
        Language,
        on_delete=models.PROTECT,
        db_column='language_id',
        related_name='language_translations',
        db_index=True
    )
    translation = models.CharField(max_length=150)

    class Meta:
        db_table = 'autocare_vcdb.language_translation'
        managed = False
        verbose_name = 'Language Translation'
        verbose_name_plural = 'Language Translations'

    def __str__(self):
        return f"LanguageTranslation {self.language_translation_id}"


class LanguageTranslationAttachment(models.Model):
    """LanguageTranslationAttachment model representing attachments for language translations."""

    language_translation_attachment_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    language_translation = models.ForeignKey(
        LanguageTranslation,
        on_delete=models.CASCADE,
        db_column='language_translation_id',
        related_name='language_translation_attachments',
        db_index=True
    )
    attachment = models.ForeignKey(
        Attachment,
        on_delete=models.PROTECT,
        db_column='attachment_id',
        related_name='language_translation_attachments',
        db_index=True
    )

    class Meta:
        db_table = 'autocare_vcdb.language_translation_attachment'
        managed = False
        verbose_name = 'Language Translation Attachment'
        verbose_name_plural = 'Language Translation Attachments'

    def __str__(self):
        return f"LanguageTranslationAttachment {self.language_translation_attachment_id}"
