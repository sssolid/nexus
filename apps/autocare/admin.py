"""
Django Admin Configuration for AutoCare Models.

This module configures the Django admin interface for Auto Care Association
database models.
"""
from django.contrib import admin
from .vcdb.models import (
    Make, VehicleType, Model, SubModel, Region, Year, Vehicle, BaseVehicle,
    DriveType, BrakeType, EngineBlock, Transmission, WheelBase, VehicleClass,
)
from .qdb.models import (
    QualifierType, Qualifier, QLanguage, QualifierTranslation,
)
from .pcdb.models import (
    Parts, PartsDescription, Category, SubCategory, Position,
)
from .padb.models import (
    PartAttribute, MetaData, MeasurementGroup, ValidValue,
)


# VCdb Admin
@admin.register(Make)
class MakeAdmin(admin.ModelAdmin):
    """Admin configuration for Make model."""
    list_display = ['make_id', 'make_name']
    search_fields = ['make_name']
    ordering = ['make_name']


@admin.register(VehicleType)
class VehicleTypeAdmin(admin.ModelAdmin):
    """Admin configuration for VehicleType model."""
    list_display = ['vehicle_type_id', 'vehicle_type_name', 'vehicle_type_group']
    list_filter = ['vehicle_type_group']
    search_fields = ['vehicle_type_name']


@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    """Admin configuration for Model."""
    list_display = ['model_id', 'model_name', 'vehicle_type']
    list_filter = ['vehicle_type']
    search_fields = ['model_name']


@admin.register(SubModel)
class SubModelAdmin(admin.ModelAdmin):
    """Admin configuration for SubModel."""
    list_display = ['sub_model_id', 'sub_model_name']
    search_fields = ['sub_model_name']


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    """Admin configuration for Region."""
    list_display = ['region_id', 'region_name', 'region_abbr', 'parent']
    list_filter = ['parent']
    search_fields = ['region_name']


@admin.register(Year)
class YearAdmin(admin.ModelAdmin):
    """Admin configuration for Year."""
    list_display = ['year_id']
    ordering = ['-year_id']


@admin.register(BaseVehicle)
class BaseVehicleAdmin(admin.ModelAdmin):
    """Admin configuration for BaseVehicle."""
    list_display = ['base_vehicle_id', 'year', 'make', 'model']
    list_filter = ['year', 'make']
    search_fields = ['base_vehicle_id']


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    """Admin configuration for Vehicle."""
    list_display = ['vehicle_id', 'base_vehicle', 'sub_model', 'region']
    list_filter = ['base_vehicle__year', 'base_vehicle__make', 'region']
    search_fields = ['vehicle_id']
    raw_id_fields = ['base_vehicle', 'sub_model', 'region']


# Qdb Admin
@admin.register(QualifierType)
class QualifierTypeAdmin(admin.ModelAdmin):
    """Admin configuration for QualifierType."""
    list_display = ['qualifier_type_id', 'qualifier_type']
    search_fields = ['qualifier_type']


@admin.register(Qualifier)
class QualifierAdmin(admin.ModelAdmin):
    """Admin configuration for Qualifier."""
    list_display = ['qualifier_id', 'qualifier_text', 'qualifier_type', 'when_modified']
    list_filter = ['qualifier_type', 'when_modified']
    search_fields = ['qualifier_text', 'example_text']
    date_hierarchy = 'when_modified'


@admin.register(QLanguage)
class QLanguageAdmin(admin.ModelAdmin):
    """Admin configuration for QLanguage."""
    list_display = ['language_id', 'language_name', 'dialect_name']
    search_fields = ['language_name', 'dialect_name']


@admin.register(QualifierTranslation)
class QualifierTranslationAdmin(admin.ModelAdmin):
    """Admin configuration for QualifierTranslation."""
    list_display = ['qualifier_translation_id', 'qualifier', 'language', 'translation_text']
    list_filter = ['language']
    search_fields = ['translation_text']
    raw_id_fields = ['qualifier', 'language']


# PCdb Admin
@admin.register(Parts)
class PartsAdmin(admin.ModelAdmin):
    """Admin configuration for Parts."""
    list_display = ['part_terminology_id', 'part_terminology_name', 'rev_date']
    search_fields = ['part_terminology_name']
    date_hierarchy = 'rev_date'


@admin.register(PartsDescription)
class PartsDescriptionAdmin(admin.ModelAdmin):
    """Admin configuration for PartsDescription."""
    list_display = ['parts_description_id', 'parts_description']
    search_fields = ['parts_description']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for Category."""
    list_display = ['category_id', 'category_name']
    search_fields = ['category_name']
    ordering = ['category_name']


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    """Admin configuration for SubCategory."""
    list_display = ['subcategory_id', 'subcategory_name']
    search_fields = ['subcategory_name']
    ordering = ['subcategory_name']


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    """Admin configuration for Position."""
    list_display = ['position_id', 'position']
    search_fields = ['position']


# PAdb Admin
@admin.register(PartAttribute)
class PartAttributeAdmin(admin.ModelAdmin):
    """Admin configuration for PartAttribute."""
    list_display = ['pa_id', 'pa_name', 'pa_descr']
    search_fields = ['pa_name', 'pa_descr']


@admin.register(MetaData)
class MetaDataAdmin(admin.ModelAdmin):
    """Admin configuration for MetaData."""
    list_display = ['meta_id', 'meta_name', 'data_type', 'meta_format']
    list_filter = ['data_type', 'meta_format']
    search_fields = ['meta_name', 'meta_descr']


@admin.register(MeasurementGroup)
class MeasurementGroupAdmin(admin.ModelAdmin):
    """Admin configuration for MeasurementGroup."""
    list_display = ['measurement_group_id', 'measurement_group_name']
    search_fields = ['measurement_group_name']


@admin.register(ValidValue)
class ValidValueAdmin(admin.ModelAdmin):
    """Admin configuration for ValidValue."""
    list_display = ['valid_value_id', 'valid_value']
    search_fields = ['valid_value']


# Note: Many junction/relationship tables are intentionally not registered
# in the admin as they are better managed through their parent models
