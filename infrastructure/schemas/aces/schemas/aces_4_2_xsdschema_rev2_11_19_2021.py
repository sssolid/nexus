from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional

from xsdata.models.datatype import XmlDate


@dataclass
class AssetItemOrder:
    value: Optional[int] = field(
        default=None,
        metadata={
            "required": True,
        },
    )


@dataclass
class AssetItemRef:
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


@dataclass
class AssetName:
    value: str = field(
        default="",
        metadata={
            "required": True,
            "min_length": 1,
            "max_length": 45,
        },
    )


@dataclass
class DisplayOrder:
    value: Optional[int] = field(
        default=None,
        metadata={
            "required": True,
        },
    )


@dataclass
class Footer:
    record_count: Optional[str] = field(
        default=None,
        metadata={
            "name": "RecordCount",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class MfrLabel:
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


@dataclass
class Qty:
    value: Optional[int] = field(
        default=None,
        metadata={
            "required": True,
        },
    )


@dataclass
class TransferDate:
    value: Optional[XmlDate] = field(
        default=None,
        metadata={
            "required": True,
        },
    )


@dataclass
class ApprovedForType:
    class Meta:
        name = "approvedForType"

    country: list[str] = field(
        default_factory=list,
        metadata={
            "name": "Country",
            "type": "Element",
            "min_occurs": 1,
            "length": 2,
        },
    )


@dataclass
class DigitalFileInformationType:
    class Meta:
        name = "digitalFileInformationType"

    file_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Element",
            "required": True,
            "min_length": 1,
            "max_length": 80,
        },
    )
    asset_detail_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "AssetDetailType",
            "type": "Element",
            "required": True,
            "length": 3,
        },
    )
    file_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "FileType",
            "type": "Element",
            "min_length": 3,
            "max_length": 4,
        },
    )
    representation: Optional[str] = field(
        default=None,
        metadata={
            "name": "Representation",
            "type": "Element",
            "length": 1,
        },
    )
    file_size: Optional[int] = field(
        default=None,
        metadata={
            "name": "FileSize",
            "type": "Element",
            "total_digits": 10,
        },
    )
    resolution: Optional[str] = field(
        default=None,
        metadata={
            "name": "Resolution",
            "type": "Element",
            "min_length": 2,
            "max_length": 4,
        },
    )
    color_mode: Optional[str] = field(
        default=None,
        metadata={
            "name": "ColorMode",
            "type": "Element",
            "length": 3,
        },
    )
    background: Optional[str] = field(
        default=None,
        metadata={
            "name": "Background",
            "type": "Element",
            "length": 3,
        },
    )
    orientation_view: Optional[str] = field(
        default=None,
        metadata={
            "name": "OrientationView",
            "type": "Element",
            "length": 3,
        },
    )
    asset_dimensions: Optional[
        "DigitalFileInformationType.AssetDimensions"
    ] = field(
        default=None,
        metadata={
            "name": "AssetDimensions",
            "type": "Element",
        },
    )
    asset_description: Optional[str] = field(
        default=None,
        metadata={
            "name": "AssetDescription",
            "type": "Element",
        },
    )
    file_path: Optional[str] = field(
        default=None,
        metadata={
            "name": "FilePath",
            "type": "Element",
            "min_length": 1,
            "max_length": 80,
        },
    )
    uri: Optional[str] = field(
        default=None,
        metadata={
            "name": "URI",
            "type": "Element",
            "max_length": 2000,
        },
    )
    file_date_modified: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "FileDateModified",
            "type": "Element",
        },
    )
    effective_date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "EffectiveDate",
            "type": "Element",
        },
    )
    expiration_date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "ExpirationDate",
            "type": "Element",
        },
    )
    country: Optional[str] = field(
        default=None,
        metadata={
            "name": "Country",
            "type": "Element",
            "length": 2,
        },
    )
    asset_name: Optional[object] = field(
        default=None,
        metadata={
            "name": "AssetName",
            "type": "Attribute",
            "required": True,
        },
    )
    action: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "length": 1,
        },
    )
    language_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "LanguageCode",
            "type": "Attribute",
        },
    )

    @dataclass
    class AssetDimensions:
        asset_height: Optional[Decimal] = field(
            default=None,
            metadata={
                "name": "AssetHeight",
                "type": "Element",
                "min_exclusive": Decimal("0"),
                "total_digits": 6,
                "fraction_digits": 4,
            },
        )
        asset_width: Optional[Decimal] = field(
            default=None,
            metadata={
                "name": "AssetWidth",
                "type": "Element",
                "min_exclusive": Decimal("0"),
                "total_digits": 6,
                "fraction_digits": 4,
            },
        )
        uom: Optional[str] = field(
            default=None,
            metadata={
                "name": "UOM",
                "type": "Attribute",
                "required": True,
                "length": 2,
            },
        )


@dataclass
class NoteType:
    class Meta:
        name = "noteType"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    id: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class ParamType:
    class Meta:
        name = "paramType"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    value_attribute: Optional[str] = field(
        default=None,
        metadata={
            "name": "value",
            "type": "Attribute",
            "required": True,
        },
    )
    uom: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "min_length": 1,
            "max_length": 3,
        },
    )
    altvalue: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    altuom: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "min_length": 1,
            "max_length": 3,
        },
    )


@dataclass
class PartNumberType:
    class Meta:
        name = "partNumberType"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "min_length": 0,
            "max_length": 45,
        },
    )
    brand_aaiaid: Optional[str] = field(
        default=None,
        metadata={
            "name": "BrandAAIAID",
            "type": "Attribute",
            "pattern": r"[B-Z-[EIOU]][B-Z-[EIO]][B-Z-[OU]][A-Z]",
        },
    )
    sub_brand_aaiaid: Optional[str] = field(
        default=None,
        metadata={
            "name": "SubBrandAAIAID",
            "type": "Attribute",
            "pattern": r"[B-Z-[EIOU]][B-Z-[EIO]][B-Z-[OU]][A-Z]",
        },
    )


@dataclass
class PartTypeType:
    """
    A Part Type references the primary key in the Parts PCdb table.
    """

    class Meta:
        name = "partTypeType"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    id: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class PositionType:
    """
    A Position references the primary key in the Position PCdb table.
    """

    class Meta:
        name = "positionType"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    id: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class VehAttrType:
    """
    Vehicle Attributes reference the primary key in the associated VCdb table.
    """

    class Meta:
        name = "vehAttrType"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    id: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class YearRangeType:
    class Meta:
        name = "yearRangeType"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    from_value: Optional[int] = field(
        default=None,
        metadata={
            "name": "from",
            "type": "Attribute",
            "required": True,
            "min_inclusive": 1896,
            "total_digits": 4,
        },
    )
    to: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "min_inclusive": 1896,
            "total_digits": 4,
        },
    )


@dataclass
class Aspiration(VehAttrType):
    pass


@dataclass
class BaseVehicle(VehAttrType):
    pass


@dataclass
class BedLength(VehAttrType):
    pass


@dataclass
class BedType(VehAttrType):
    pass


@dataclass
class BodyNumDoors(VehAttrType):
    pass


@dataclass
class BodyType(VehAttrType):
    pass


@dataclass
class BrakeAbs(VehAttrType):
    class Meta:
        name = "BrakeABS"


@dataclass
class BrakeSystem(VehAttrType):
    pass


@dataclass
class CylinderHeadType(VehAttrType):
    pass


@dataclass
class DigitalAsset:
    digital_file_information: list[DigitalFileInformationType] = field(
        default_factory=list,
        metadata={
            "name": "DigitalFileInformation",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class DriveType(VehAttrType):
    pass


@dataclass
class EngineBase(VehAttrType):
    pass


@dataclass
class EngineBlock(VehAttrType):
    pass


@dataclass
class EngineBoreStroke(VehAttrType):
    pass


@dataclass
class EngineDesignation(VehAttrType):
    pass


@dataclass
class EngineMfr(VehAttrType):
    pass


@dataclass
class EngineVin(VehAttrType):
    class Meta:
        name = "EngineVIN"


@dataclass
class EngineVersion(VehAttrType):
    pass


@dataclass
class EquipmentBase(VehAttrType):
    pass


@dataclass
class EquipmentModel(VehAttrType):
    pass


@dataclass
class FrontBrakeType(VehAttrType):
    pass


@dataclass
class FrontSpringType(VehAttrType):
    pass


@dataclass
class FuelDeliverySubType(VehAttrType):
    pass


@dataclass
class FuelDeliveryType(VehAttrType):
    pass


@dataclass
class FuelSystemControlType(VehAttrType):
    pass


@dataclass
class FuelSystemDesign(VehAttrType):
    pass


@dataclass
class FuelType(VehAttrType):
    pass


@dataclass
class IgnitionSystemType(VehAttrType):
    pass


@dataclass
class Make(VehAttrType):
    pass


@dataclass
class Mfr(VehAttrType):
    pass


@dataclass
class MfrBodyCode(VehAttrType):
    pass


@dataclass
class Model(VehAttrType):
    pass


@dataclass
class Note(NoteType):
    pass


@dataclass
class Part(PartNumberType):
    pass


@dataclass
class PartType(PartTypeType):
    pass


@dataclass
class Position(PositionType):
    pass


@dataclass
class PowerOutput(VehAttrType):
    pass


@dataclass
class RearBrakeType(VehAttrType):
    pass


@dataclass
class RearSpringType(VehAttrType):
    pass


@dataclass
class Region(VehAttrType):
    pass


@dataclass
class SteeringSystem(VehAttrType):
    pass


@dataclass
class SteeringType(VehAttrType):
    pass


@dataclass
class SubModel(VehAttrType):
    pass


@dataclass
class TransElecControlled(VehAttrType):
    pass


@dataclass
class TransmissionBase(VehAttrType):
    pass


@dataclass
class TransmissionControlType(VehAttrType):
    pass


@dataclass
class TransmissionMfr(VehAttrType):
    pass


@dataclass
class TransmissionMfrCode(VehAttrType):
    pass


@dataclass
class TransmissionNumSpeeds(VehAttrType):
    pass


@dataclass
class TransmissionType(VehAttrType):
    pass


@dataclass
class ValvesPerEngine(VehAttrType):
    pass


@dataclass
class VehicleType(VehAttrType):
    pass


@dataclass
class WheelBase(VehAttrType):
    pass


@dataclass
class Years(YearRangeType):
    pass


@dataclass
class QualType:
    class Meta:
        name = "qualType"

    param: list[ParamType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    text: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    id: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Qual(QualType):
    pass


@dataclass
class RegionType:
    region: list[Region] = field(
        default_factory=list,
        metadata={
            "name": "Region",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Header:
    company: Optional[str] = field(
        default=None,
        metadata={
            "name": "Company",
            "type": "Element",
            "required": True,
        },
    )
    sender_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "SenderName",
            "type": "Element",
            "required": True,
        },
    )
    sender_phone: Optional[str] = field(
        default=None,
        metadata={
            "name": "SenderPhone",
            "type": "Element",
            "required": True,
        },
    )
    sender_phone_ext: Optional[str] = field(
        default=None,
        metadata={
            "name": "SenderPhoneExt",
            "type": "Element",
        },
    )
    transfer_date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "TransferDate",
            "type": "Element",
            "required": True,
        },
    )
    mfr_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "MfrCode",
            "type": "Element",
        },
    )
    brand_aaiaid: Optional[str] = field(
        default=None,
        metadata={
            "name": "BrandAAIAID",
            "type": "Element",
            "pattern": r"[B-Z-[EIOU]][B-Z-[EIO]][B-Z-[OU]][A-Z]",
        },
    )
    sub_brand_aaiaid: Optional[str] = field(
        default=None,
        metadata={
            "name": "SubBrandAAIAID",
            "type": "Element",
            "pattern": r"[B-Z-[EIOU]][B-Z-[EIO]][B-Z-[OU]][A-Z]",
        },
    )
    document_title: Optional[str] = field(
        default=None,
        metadata={
            "name": "DocumentTitle",
            "type": "Element",
            "required": True,
        },
    )
    doc_form_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "DocFormNumber",
            "type": "Element",
        },
    )
    effective_date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "EffectiveDate",
            "type": "Element",
            "required": True,
        },
    )
    approved_for: Optional[ApprovedForType] = field(
        default=None,
        metadata={
            "name": "ApprovedFor",
            "type": "Element",
        },
    )
    parts_approved_for: Optional[ApprovedForType] = field(
        default=None,
        metadata={
            "name": "PartsApprovedFor",
            "type": "Element",
        },
    )
    region_for: Optional[RegionType] = field(
        default=None,
        metadata={
            "name": "RegionFor",
            "type": "Element",
        },
    )
    submission_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "SubmissionType",
            "type": "Element",
            "required": True,
            "min_length": 4,
            "max_length": 6,
        },
    )
    mapper_company: Optional[str] = field(
        default=None,
        metadata={
            "name": "MapperCompany",
            "type": "Element",
        },
    )
    mapper_contact: Optional[str] = field(
        default=None,
        metadata={
            "name": "MapperContact",
            "type": "Element",
        },
    )
    mapper_phone: Optional[str] = field(
        default=None,
        metadata={
            "name": "MapperPhone",
            "type": "Element",
        },
    )
    mapper_phone_ext: Optional[str] = field(
        default=None,
        metadata={
            "name": "MapperPhoneExt",
            "type": "Element",
        },
    )
    mapper_email: Optional[str] = field(
        default=None,
        metadata={
            "name": "MapperEmail",
            "type": "Element",
        },
    )
    vcdb_version_date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "VcdbVersionDate",
            "type": "Element",
            "required": True,
        },
    )
    qdb_version_date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "QdbVersionDate",
            "type": "Element",
            "required": True,
        },
    )
    pcdb_version_date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "PcdbVersionDate",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class AppItemsBaseType:
    class Meta:
        name = "appItemsBaseType"

    base_vehicle: Optional[BaseVehicle] = field(
        default=None,
        metadata={
            "name": "BaseVehicle",
            "type": "Element",
        },
    )
    sub_model: list[SubModel] = field(
        default_factory=list,
        metadata={
            "name": "SubModel",
            "type": "Element",
            "max_occurs": 2,
        },
    )
    years: Optional[Years] = field(
        default=None,
        metadata={
            "name": "Years",
            "type": "Element",
        },
    )
    make: Optional[Make] = field(
        default=None,
        metadata={
            "name": "Make",
            "type": "Element",
        },
    )
    vehicle_type: list[VehicleType] = field(
        default_factory=list,
        metadata={
            "name": "VehicleType",
            "type": "Element",
            "max_occurs": 2,
        },
    )
    model: Optional[Model] = field(
        default=None,
        metadata={
            "name": "Model",
            "type": "Element",
        },
    )
    equipment_base: Optional[EquipmentBase] = field(
        default=None,
        metadata={
            "name": "EquipmentBase",
            "type": "Element",
        },
    )
    mfr: Optional[Mfr] = field(
        default=None,
        metadata={
            "name": "Mfr",
            "type": "Element",
        },
    )
    equipment_model: Optional[EquipmentModel] = field(
        default=None,
        metadata={
            "name": "EquipmentModel",
            "type": "Element",
        },
    )
    production_years: Optional["AppItemsBaseType.ProductionYears"] = field(
        default=None,
        metadata={
            "name": "ProductionYears",
            "type": "Element",
        },
    )
    mfr_body_code: Optional[MfrBodyCode] = field(
        default=None,
        metadata={
            "name": "MfrBodyCode",
            "type": "Element",
        },
    )
    body_num_doors: Optional[BodyNumDoors] = field(
        default=None,
        metadata={
            "name": "BodyNumDoors",
            "type": "Element",
        },
    )
    body_type: Optional[BodyType] = field(
        default=None,
        metadata={
            "name": "BodyType",
            "type": "Element",
        },
    )
    drive_type: Optional[DriveType] = field(
        default=None,
        metadata={
            "name": "DriveType",
            "type": "Element",
        },
    )
    engine_base: Optional[EngineBase] = field(
        default=None,
        metadata={
            "name": "EngineBase",
            "type": "Element",
        },
    )
    engine_block: Optional[EngineBlock] = field(
        default=None,
        metadata={
            "name": "EngineBlock",
            "type": "Element",
        },
    )
    engine_bore_stroke: Optional[EngineBoreStroke] = field(
        default=None,
        metadata={
            "name": "EngineBoreStroke",
            "type": "Element",
        },
    )
    engine_designation: Optional[EngineDesignation] = field(
        default=None,
        metadata={
            "name": "EngineDesignation",
            "type": "Element",
        },
    )
    engine_vin: Optional[EngineVin] = field(
        default=None,
        metadata={
            "name": "EngineVIN",
            "type": "Element",
        },
    )
    engine_version: Optional[EngineVersion] = field(
        default=None,
        metadata={
            "name": "EngineVersion",
            "type": "Element",
        },
    )
    engine_mfr: Optional[EngineMfr] = field(
        default=None,
        metadata={
            "name": "EngineMfr",
            "type": "Element",
        },
    )
    power_output: Optional[PowerOutput] = field(
        default=None,
        metadata={
            "name": "PowerOutput",
            "type": "Element",
        },
    )
    valves_per_engine: Optional[ValvesPerEngine] = field(
        default=None,
        metadata={
            "name": "ValvesPerEngine",
            "type": "Element",
        },
    )
    fuel_delivery_type: Optional[FuelDeliveryType] = field(
        default=None,
        metadata={
            "name": "FuelDeliveryType",
            "type": "Element",
        },
    )
    fuel_delivery_sub_type: Optional[FuelDeliverySubType] = field(
        default=None,
        metadata={
            "name": "FuelDeliverySubType",
            "type": "Element",
        },
    )
    fuel_system_control_type: Optional[FuelSystemControlType] = field(
        default=None,
        metadata={
            "name": "FuelSystemControlType",
            "type": "Element",
        },
    )
    fuel_system_design: Optional[FuelSystemDesign] = field(
        default=None,
        metadata={
            "name": "FuelSystemDesign",
            "type": "Element",
        },
    )
    aspiration: Optional[Aspiration] = field(
        default=None,
        metadata={
            "name": "Aspiration",
            "type": "Element",
        },
    )
    cylinder_head_type: Optional[CylinderHeadType] = field(
        default=None,
        metadata={
            "name": "CylinderHeadType",
            "type": "Element",
        },
    )
    fuel_type: Optional[FuelType] = field(
        default=None,
        metadata={
            "name": "FuelType",
            "type": "Element",
        },
    )
    ignition_system_type: Optional[IgnitionSystemType] = field(
        default=None,
        metadata={
            "name": "IgnitionSystemType",
            "type": "Element",
        },
    )
    transmission_mfr_code: Optional[TransmissionMfrCode] = field(
        default=None,
        metadata={
            "name": "TransmissionMfrCode",
            "type": "Element",
        },
    )
    transmission_base: Optional[TransmissionBase] = field(
        default=None,
        metadata={
            "name": "TransmissionBase",
            "type": "Element",
        },
    )
    transmission_type: Optional[TransmissionType] = field(
        default=None,
        metadata={
            "name": "TransmissionType",
            "type": "Element",
        },
    )
    transmission_control_type: Optional[TransmissionControlType] = field(
        default=None,
        metadata={
            "name": "TransmissionControlType",
            "type": "Element",
        },
    )
    transmission_num_speeds: Optional[TransmissionNumSpeeds] = field(
        default=None,
        metadata={
            "name": "TransmissionNumSpeeds",
            "type": "Element",
        },
    )
    trans_elec_controlled: Optional[TransElecControlled] = field(
        default=None,
        metadata={
            "name": "TransElecControlled",
            "type": "Element",
        },
    )
    transmission_mfr: Optional[TransmissionMfr] = field(
        default=None,
        metadata={
            "name": "TransmissionMfr",
            "type": "Element",
        },
    )
    bed_length: Optional[BedLength] = field(
        default=None,
        metadata={
            "name": "BedLength",
            "type": "Element",
        },
    )
    bed_type: Optional[BedType] = field(
        default=None,
        metadata={
            "name": "BedType",
            "type": "Element",
        },
    )
    wheel_base: Optional[WheelBase] = field(
        default=None,
        metadata={
            "name": "WheelBase",
            "type": "Element",
        },
    )
    brake_system: Optional[BrakeSystem] = field(
        default=None,
        metadata={
            "name": "BrakeSystem",
            "type": "Element",
        },
    )
    front_brake_type: Optional[FrontBrakeType] = field(
        default=None,
        metadata={
            "name": "FrontBrakeType",
            "type": "Element",
        },
    )
    rear_brake_type: Optional[RearBrakeType] = field(
        default=None,
        metadata={
            "name": "RearBrakeType",
            "type": "Element",
        },
    )
    brake_abs: Optional[BrakeAbs] = field(
        default=None,
        metadata={
            "name": "BrakeABS",
            "type": "Element",
        },
    )
    front_spring_type: Optional[FrontSpringType] = field(
        default=None,
        metadata={
            "name": "FrontSpringType",
            "type": "Element",
        },
    )
    rear_spring_type: Optional[RearSpringType] = field(
        default=None,
        metadata={
            "name": "RearSpringType",
            "type": "Element",
        },
    )
    steering_system: Optional[SteeringSystem] = field(
        default=None,
        metadata={
            "name": "SteeringSystem",
            "type": "Element",
        },
    )
    steering_type: Optional[SteeringType] = field(
        default=None,
        metadata={
            "name": "SteeringType",
            "type": "Element",
        },
    )
    region: Optional[Region] = field(
        default=None,
        metadata={
            "name": "Region",
            "type": "Element",
        },
    )
    qual: list[Qual] = field(
        default_factory=list,
        metadata={
            "name": "Qual",
            "type": "Element",
        },
    )
    note: list[Note] = field(
        default_factory=list,
        metadata={
            "name": "Note",
            "type": "Element",
        },
    )
    action: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "length": 1,
        },
    )
    id: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    ref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    validate_value: str = field(
        default="yes",
        metadata={
            "name": "validate",
            "type": "Attribute",
            "min_length": 2,
            "max_length": 3,
        },
    )

    @dataclass
    class ProductionYears:
        production_start: Optional[int] = field(
            default=None,
            metadata={
                "name": "ProductionStart",
                "type": "Attribute",
                "min_inclusive": 1896,
                "total_digits": 4,
            },
        )
        production_end: Optional[int] = field(
            default=None,
            metadata={
                "name": "ProductionEnd",
                "type": "Attribute",
                "min_inclusive": 1896,
                "total_digits": 4,
            },
        )


@dataclass
class AppType(AppItemsBaseType):
    class Meta:
        name = "appType"

    qty: Optional[Qty] = field(
        default=None,
        metadata={
            "name": "Qty",
            "type": "Element",
            "required": True,
        },
    )
    part_type: Optional[PartType] = field(
        default=None,
        metadata={
            "name": "PartType",
            "type": "Element",
            "required": True,
        },
    )
    mfr_label: Optional[MfrLabel] = field(
        default=None,
        metadata={
            "name": "MfrLabel",
            "type": "Element",
        },
    )
    position: Optional[Position] = field(
        default=None,
        metadata={
            "name": "Position",
            "type": "Element",
        },
    )
    part: Optional[Part] = field(
        default=None,
        metadata={
            "name": "Part",
            "type": "Element",
            "required": True,
        },
    )
    display_order: Optional[DisplayOrder] = field(
        default=None,
        metadata={
            "name": "DisplayOrder",
            "type": "Element",
        },
    )
    asset_name: Optional[AssetName] = field(
        default=None,
        metadata={
            "name": "AssetName",
            "type": "Element",
        },
    )
    asset_item_order: Optional[AssetItemOrder] = field(
        default=None,
        metadata={
            "name": "AssetItemOrder",
            "type": "Element",
        },
    )
    asset_item_ref: Optional[AssetItemRef] = field(
        default=None,
        metadata={
            "name": "AssetItemRef",
            "type": "Element",
        },
    )


@dataclass
class AssetType(AppItemsBaseType):
    class Meta:
        name = "assetType"


@dataclass
class App(AppType):
    pass


@dataclass
class Asset(AssetType):
    asset_name: Optional[AssetName] = field(
        default=None,
        metadata={
            "name": "AssetName",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Aces:
    class Meta:
        name = "ACES"

    header: Optional[Header] = field(
        default=None,
        metadata={
            "name": "Header",
            "type": "Element",
            "required": True,
        },
    )
    app: list[App] = field(
        default_factory=list,
        metadata={
            "name": "App",
            "type": "Element",
        },
    )
    asset: list[Asset] = field(
        default_factory=list,
        metadata={
            "name": "Asset",
            "type": "Element",
        },
    )
    digital_asset: Optional[DigitalAsset] = field(
        default=None,
        metadata={
            "name": "DigitalAsset",
            "type": "Element",
        },
    )
    footer: Optional[Footer] = field(
        default=None,
        metadata={
            "name": "Footer",
            "type": "Element",
            "required": True,
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "min_length": 3,
            "max_length": 5,
        },
    )
