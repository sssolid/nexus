"""
Django Admin for ACES Applications with VCdb Integration

This admin interface provides a comprehensive view of ACES data
with all IDs resolved to actual VCdb names for easy reading.

Part lookup is integrated directly into the admin - no manual URL configuration needed!
"""

from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Prefetch
from django.urls import path, reverse
from django.shortcuts import render
from django.utils.safestring import mark_safe

from apps.autocare.aces.models import (
    AcesApp,
    AcesAppVehicle,
    AcesQualifier,
    AcesRawAttribute,
    AcesVehicleType,
)

from apps.autocare.vcdb.models.make import Make
from apps.autocare.vcdb.models.model import VehicleModel
from apps.autocare.vcdb.models.sub_model import SubModel
from apps.autocare.vcdb.models.year import Year
from apps.autocare.vcdb.models.base_vehicle import BaseVehicle
from apps.autocare.vcdb.models.engine_base import EngineBase
from apps.autocare.vcdb.models.engine_block import EngineBlock
from apps.autocare.vcdb.models.engine_vin import EngineVIN
from apps.autocare.vcdb.models.aspiration import Aspiration
from apps.autocare.vcdb.models.transmission_base import TransmissionBase
from apps.autocare.vcdb.models.transmission_type import TransmissionType
from apps.autocare.vcdb.models.drive_type import DriveType
from apps.autocare.vcdb.models.fuel_type import FuelType
from apps.autocare.vcdb.models.steering_type import SteeringType
from apps.autocare.vcdb.models.brake_abs import BrakeABS
from apps.autocare.vcdb.models.brake_system import BrakeSystem
from apps.autocare.vcdb.models.body_type import BodyType
from apps.autocare.vcdb.models.bed_type import BedType
from apps.autocare.vcdb.models.wheel_base import WheelBase
from apps.autocare.vcdb.models.region import Region
from apps.autocare.vcdb.models.vehicle_type import VehicleType


# =====================================================
# INLINE DISPLAYS
# =====================================================

class AcesQualifierInline(admin.TabularInline):
    """Display qualifiers for an application"""
    model = AcesQualifier
    extra = 0
    fields = ('qual_id', 'qual_text', 'param_1', 'param_2', 'param_3')
    readonly_fields = fields
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


class AcesNoteInline(admin.TabularInline):
    """Display notes for an application"""
    model = AcesRawAttribute
    extra = 0
    fields = ('note_display', 'attr_id', 'idx')
    readonly_fields = fields
    can_delete = False
    verbose_name = "Note"
    verbose_name_plural = "Notes"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(attr_name='note').order_by('idx')

    def note_display(self, obj):
        return obj.attr_value or ''
    note_display.short_description = 'Note Text'

    def has_add_permission(self, request, obj=None):
        return False


class AcesVehicleTypeInline(admin.TabularInline):
    """Display vehicle types for an application"""
    model = AcesVehicleType
    extra = 0
    fields = ('vehicle_type_display', 'idx')
    readonly_fields = fields
    can_delete = False
    verbose_name = "Vehicle Type"
    verbose_name_plural = "Vehicle Types"

    def vehicle_type_display(self, obj):
        try:
            vt = VehicleType.objects.get(vehicle_type_id=obj.vehicle_type_id)
            return f"{vt.vehicle_type_name} (ID: {obj.vehicle_type_id})"
        except:
            return f"Vehicle Type ID: {obj.vehicle_type_id}"
    vehicle_type_display.short_description = 'Vehicle Type'

    def has_add_permission(self, request, obj=None):
        return False


class AcesRawAttributeInline(admin.TabularInline):
    """Display raw/unmapped attributes"""
    model = AcesRawAttribute
    extra = 0
    fields = ('attr_name', 'attr_id', 'attr_value', 'idx')
    readonly_fields = fields
    can_delete = False
    verbose_name = "Raw Attribute"
    verbose_name_plural = "Raw Attributes (Unmapped)"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.exclude(attr_name='note').order_by('attr_name', 'idx')

    def has_add_permission(self, request, obj=None):
        return False


# =====================================================
# VEHICLE INLINE WITH VCDB RESOLUTION
# =====================================================

class AcesAppVehicleInline(admin.StackedInline):
    """Display vehicle information with VCdb names"""
    model = AcesAppVehicle
    extra = 0
    can_delete = False

    fieldsets = (
        ('Primary Vehicle Identification', {
            'fields': (
                'base_vehicle_display',
                'year_range_display',
                'make_display',
                'model_display',
                'submodel_display',
            ),
            'classes': ('wide',),
        }),
        ('Engine Specifications', {
            'fields': (
                'engine_base_display',
                'engine_block_display',
                'engine_vin_display',
                'aspiration_display',
            ),
            'classes': ('collapse',),
        }),
        ('Transmission', {
            'fields': (
                'transmission_base_display',
                'transmission_type_display',
            ),
            'classes': ('collapse',),
        }),
        ('Drivetrain & Other', {
            'fields': (
                'drive_type_display',
                'fuel_type_display',
            ),
            'classes': ('collapse',),
        }),
    )

    readonly_fields = (
        'base_vehicle_display', 'year_range_display', 'make_display',
        'model_display', 'submodel_display', 'engine_base_display',
        'engine_block_display', 'engine_vin_display', 'aspiration_display',
        'transmission_base_display', 'transmission_type_display',
        'drive_type_display', 'fuel_type_display',
    )

    def base_vehicle_display(self, obj):
        if obj.base_vehicle:
            try:
                bv = obj.base_vehicle
                return format_html(
                    '<strong style="color: #0066cc; font-size: 14px;">{}</strong><br>'
                    '<small style="color: #666;">Base Vehicle ID: {}</small>',
                    bv.get_display_name(),
                    obj.base_vehicle_id
                )
            except:
                return f"Base Vehicle ID: {obj.base_vehicle_id}"
        return '-'
    base_vehicle_display.short_description = 'Base Vehicle'

    def year_range_display(self, obj):
        if obj.year_from and obj.year_to:
            if obj.year_from == obj.year_to:
                return format_html('<strong>{}</strong>', obj.year_from)
            return format_html('<strong>{} - {}</strong>', obj.year_from, obj.year_to)
        elif obj.year_from:
            return format_html('<strong>{}</strong>', obj.year_from)
        return '-'
    year_range_display.short_description = 'Year(s)'

    def make_display(self, obj):
        if obj.make:
            try:
                return f"{obj.make.make_name} (ID: {obj.make_id})"
            except:
                return f"Make ID: {obj.make_id}"
        return '-'
    make_display.short_description = 'Make'

    def model_display(self, obj):
        if obj.model:
            try:
                return f"{obj.model.model_name} (ID: {obj.model_id})"
            except:
                return f"Model ID: {obj.model_id}"
        return '-'
    model_display.short_description = 'Model'

    def submodel_display(self, obj):
        if obj.submodel:
            try:
                return f"{obj.submodel.submodel_name} (ID: {obj.submodel_id})"
            except:
                return f"SubModel ID: {obj.submodel_id}"
        return '-'
    submodel_display.short_description = 'SubModel / Trim'

    def engine_base_display(self, obj):
        if obj.engine_base_id:
            try:
                eng = EngineBase.objects.get(engine_base_id=obj.engine_base_id)
                return format_html(
                    '<strong>{}</strong><br><small>ID: {}</small>',
                    str(eng),
                    obj.engine_base_id
                )
            except:
                return f"Engine Base ID: {obj.engine_base_id}"
        return '-'
    engine_base_display.short_description = 'Engine Base'

    def engine_block_display(self, obj):
        if obj.engine_block_id:
            try:
                block = EngineBlock.objects.get(engine_block_id=obj.engine_block_id)
                return f"{block} (ID: {obj.engine_block_id})"
            except:
                return f"Engine Block ID: {obj.engine_block_id}"
        return '-'
    engine_block_display.short_description = 'Engine Block'

    def engine_vin_display(self, obj):
        if obj.engine_vin_id:
            try:
                vin = EngineVIN.objects.get(engine_vin_id=obj.engine_vin_id)
                return f"{vin} (ID: {obj.engine_vin_id})"
            except:
                return f"Engine VIN ID: {obj.engine_vin_id}"
        return '-'
    engine_vin_display.short_description = 'Engine VIN'

    def aspiration_display(self, obj):
        if obj.aspiration_id:
            try:
                asp = Aspiration.objects.get(aspiration_id=obj.aspiration_id)
                return f"{asp} (ID: {obj.aspiration_id})"
            except:
                return f"Aspiration ID: {obj.aspiration_id}"
        return '-'
    aspiration_display.short_description = 'Aspiration'

    def transmission_base_display(self, obj):
        if obj.transmission_base_id:
            try:
                trans = TransmissionBase.objects.get(transmission_base_id=obj.transmission_base_id)
                return f"{trans} (ID: {obj.transmission_base_id})"
            except:
                return f"Transmission Base ID: {obj.transmission_base_id}"
        return '-'
    transmission_base_display.short_description = 'Transmission Base'

    def transmission_type_display(self, obj):
        if obj.transmission_type_id:
            try:
                trans_type = TransmissionType.objects.get(transmission_type_id=obj.transmission_type_id)
                return f"{trans_type} (ID: {obj.transmission_type_id})"
            except:
                return f"Transmission Type ID: {obj.transmission_type_id}"
        return '-'
    transmission_type_display.short_description = 'Transmission Type'

    def drive_type_display(self, obj):
        if obj.drive_type_id:
            try:
                drive = DriveType.objects.get(drive_type_id=obj.drive_type_id)
                return f"{drive} (ID: {obj.drive_type_id})"
            except:
                return f"Drive Type ID: {obj.drive_type_id}"
        return '-'
    drive_type_display.short_description = 'Drive Type'

    def fuel_type_display(self, obj):
        if obj.fuel_type_id:
            try:
                fuel = FuelType.objects.get(fuel_type_id=obj.fuel_type_id)
                return f"{fuel} (ID: {obj.fuel_type_id})"
            except:
                return f"Fuel Type ID: {obj.fuel_type_id}"
        return '-'
    fuel_type_display.short_description = 'Fuel Type'

    def has_add_permission(self, request, obj=None):
        return False


# =====================================================
# MAIN ACES APPLICATION ADMIN
# =====================================================

@admin.register(AcesApp)
class AcesAppAdmin(admin.ModelAdmin):
    """Main admin for ACES Applications with integrated part lookup"""

    # Change list button for part lookup
    change_list_template = 'admin/aces/acesapp_changelist.html'

    list_display = (
        'app_id_display',
        'part_number_display',
        'part_type_display',
        'vehicle_summary',
        'qualifier_count',
        'note_count',
        'validate_display',
    )

    list_filter = (
        'validate',
        'action',
        'source_file',
    )

    search_fields = (
        'part_number',
        'app_id',
        'mfr_label',
    )

    readonly_fields = (
        'app_id',
        'source_file',
        'action',
        'validate',
        'part_number',
        'part_type_id',
        'quantity',
        'position_id',
        'brand_aaiaid',
        'subbrand_aaiaid',
        'mfr_label',
        'display_order',
        'asset_name',
        'asset_item_order',
        'asset_item_ref',
        'vehicle_summary_full',
    )

    fieldsets = (
        ('Application Identification', {
            'fields': (
                'app_id',
                'source_file',
                'action',
                'validate',
            ),
        }),
        ('Part Information', {
            'fields': (
                'part_number',
                'part_type_id',
                'quantity',
                'position_id',
                'mfr_label',
            ),
        }),
        ('Brand Information', {
            'fields': (
                'brand_aaiaid',
                'subbrand_aaiaid',
            ),
            'classes': ('collapse',),
        }),
        ('Asset Information', {
            'fields': (
                'display_order',
                'asset_name',
                'asset_item_order',
                'asset_item_ref',
            ),
            'classes': ('collapse',),
        }),
        ('Vehicle Summary', {
            'fields': (
                'vehicle_summary_full',
            ),
        }),
    )

    inlines = [
        AcesAppVehicleInline,
        AcesQualifierInline,
        AcesNoteInline,
        AcesVehicleTypeInline,
        AcesRawAttributeInline,
    ]

    # =====================================================
    # CUSTOM URL INTEGRATION - THE PROPER WAY
    # =====================================================

    def get_urls(self):
        """Add custom admin URLs the Django way"""
        urls = super().get_urls()
        custom_urls = [
            path(
                'part-lookup/',
                self.admin_site.admin_view(self.part_lookup_view),
                name='acesapp_part_lookup',
            ),
        ]
        return custom_urls + urls

    def part_lookup_view(self, request):
        """Enhanced part number lookup with filtering, sorting, and comprehensive data"""
        from django.core.paginator import Paginator
        from django.db.models import Q
        from django.shortcuts import render
        import traceback

        context = dict(
            self.admin_site.each_context(request),
            title='Part Number Application Lookup',
        )

        part_number = request.GET.get('part_number', '').strip()

        if not part_number:
            return render(request, 'admin/aces/part_lookup.html', context)

        # Get filter parameters
        year_filter = request.GET.get('year', '')
        make_filter = request.GET.get('make', '')
        model_filter = request.GET.get('model', '')
        sort_by = request.GET.get('sort', 'year')
        page_num = request.GET.get('page', 1)

        # Base queryset
        apps = AcesApp.objects.filter(
            part_number__iexact=part_number
        ).select_related(
            'acesappvehicle__base_vehicle__vehicle_year',
            'acesappvehicle__base_vehicle__make',
            'acesappvehicle__base_vehicle__vehicle_model',
            'acesappvehicle__make',
            'acesappvehicle__model',
            'acesappvehicle__submodel',
        ).prefetch_related(
            'qualifiers',
            Prefetch(
                'raw_attributes',
                queryset=AcesRawAttribute.objects.filter(attr_name='note').order_by('idx'),
                to_attr='note_list'
            ),
            'vehicle_types',
        )

        # Apply filters if provided
        if year_filter:
            apps = apps.filter(
                Q(acesappvehicle__year_from__lte=int(year_filter)) &
                Q(acesappvehicle__year_to__gte=int(year_filter))
            )
        if make_filter:
            apps = apps.filter(acesappvehicle__make__make_id=int(make_filter))
        if model_filter:
            apps = apps.filter(acesappvehicle__model__model_id=int(model_filter))

        # Get total count
        total_count = apps.count()

        # Enrich applications with VCdb data
        enriched_apps = []
        year_set = set()
        make_dict = {}
        model_dict = {}
        errors = []

        for app in apps:
            app_data = {
                'app': app,
                'vehicle': {},
                'qualifiers': list(app.qualifiers.all()),
                'notes': getattr(app, 'note_list', []),
            }

            try:
                vehicle = app.acesappvehicle

                # YEARS
                if vehicle.year_from:
                    year_set.add(vehicle.year_from)
                    if vehicle.year_to and vehicle.year_to != vehicle.year_from:
                        for y in range(vehicle.year_from, vehicle.year_to + 1):
                            year_set.add(y)
                        app_data['vehicle']['years'] = f"{vehicle.year_from}-{vehicle.year_to}"
                        app_data['vehicle']['year_from'] = vehicle.year_from
                        app_data['vehicle']['year_to'] = vehicle.year_to
                    else:
                        app_data['vehicle']['years'] = str(vehicle.year_from)
                        app_data['vehicle']['year_from'] = vehicle.year_from
                        app_data['vehicle']['year_to'] = vehicle.year_from

                # BASE VEHICLE
                if vehicle.base_vehicle:
                    try:
                        bv = vehicle.base_vehicle
                        try:
                            year_val = bv.vehicle_year.year_id if hasattr(bv, 'vehicle_year') else None
                            make_val = bv.make.make_name if hasattr(bv, 'make') else None
                            model_val = bv.vehicle_model.model_name if hasattr(bv, 'vehicle_model') else None

                            if year_val and make_val and model_val:
                                app_data['vehicle']['base_vehicle'] = f"{year_val} {make_val} {model_val}"
                                app_data['vehicle']['year_obj'] = year_val
                                app_data['vehicle']['make_obj'] = make_val
                                app_data['vehicle']['make_id'] = bv.make.make_id
                                app_data['vehicle']['model_obj'] = model_val
                                app_data['vehicle']['model_id'] = bv.vehicle_model.model_id

                                year_set.add(year_val)
                                make_dict[bv.make.make_id] = make_val
                                model_dict[bv.vehicle_model.model_id] = model_val
                            else:
                                errors.append(f"BaseVehicle {vehicle.base_vehicle_id if vehicle.base_vehicle else None} missing a field")
                                app_data['vehicle']['base_vehicle'] = f"Base Vehicle ID: {vehicle.base_vehicle_id if vehicle.base_vehicle else None}"
                        except Exception as e:
                            errors.append(f"BaseVehicle {vehicle.base_vehicle_id if vehicle.base_vehicle else None} field access error: {str(e)}")
                            app_data['vehicle']['base_vehicle'] = f"Base Vehicle ID: {vehicle.base_vehicle_id if vehicle.base_vehicle else None}"
                    except BaseVehicle.DoesNotExist:
                        errors.append(f"BaseVehicle {vehicle.base_vehicle_id if vehicle.base_vehicle else None} does not exist")
                        app_data['vehicle']['base_vehicle'] = f"Base Vehicle ID: {vehicle.base_vehicle_id if vehicle.base_vehicle else None} (not found)"
                    except Exception as e:
                        errors.append(f"BaseVehicle lookup error: {str(e)}")
                        app_data['vehicle']['base_vehicle'] = f"Base Vehicle ID: {vehicle.base_vehicle_id if vehicle.base_vehicle else None}"

                # MAKE
                if vehicle.make and 'make_obj' not in app_data['vehicle']:
                    try:
                        make = vehicle.make
                        app_data['vehicle']['make_obj'] = make.make_name
                        app_data['vehicle']['make_id'] = make.make_id
                        make_dict[make.make_id] = make.make_name
                    except Make.DoesNotExist:
                        app_data['vehicle']['make_obj'] = f"Make ID: {vehicle.make}"
                    except Exception as e:
                        errors.append(f"Make lookup error: {str(e)}")
                        app_data['vehicle']['make_obj'] = f"Make ID: {vehicle.make}"

                # MODEL
                if vehicle.model and 'model_obj' not in app_data['vehicle']:
                    try:
                        model = vehicle.model
                        app_data['vehicle']['model_obj'] = model.model_name
                        app_data['vehicle']['model_id'] = model.model_id
                        model_dict[model.model_id] = model.model_name
                    except VehicleModel.DoesNotExist:
                        app_data['vehicle']['model_obj'] = f"Model ID: {vehicle.model}"
                    except Exception as e:
                        errors.append(f"Model lookup error: {str(e)}")
                        app_data['vehicle']['model_obj'] = f"Model ID: {vehicle.model}"

                # SUBMODEL
                if vehicle.submodel:
                    try:
                        submodel = vehicle.submodel
                        app_data['vehicle']['submodel'] = submodel.sub_model_name
                        app_data['vehicle']['submodel_id'] = vehicle.submodel
                    except SubModel.DoesNotExist:
                        app_data['vehicle']['submodel'] = f"SubModel ID: {vehicle.submodel}"
                    except Exception as e:
                        errors.append(f"SubModel lookup error: {str(e)}")

                # ENGINE BASE
                if vehicle.engine_base_id:
                    try:
                        engine = EngineBase.objects.get(engine_base_id=vehicle.engine_base_id)
                        app_data['vehicle']['engine'] = {
                            'display': f"{engine.block_type}{engine.cylinders}-{engine.liter}L ({engine.c_id}ci)",
                            'liter': engine.liter,
                            'cid': engine.c_id,
                            'cylinders': engine.cylinders,
                            'block_type': engine.block_type,
                        }
                    except EngineBase.DoesNotExist:
                        app_data['vehicle']['engine'] = {'display': f"Engine ID: {vehicle.engine_base_id}"}
                    except Exception as e:
                        errors.append(f"Engine lookup error: {str(e)}")
                        app_data['vehicle']['engine'] = {'display': f"Engine ID: {vehicle.engine_base_id}"}

                # ENGINE BLOCK (fallback)
                if vehicle.engine_block_id and 'engine' not in app_data['vehicle']:
                    try:
                        block = EngineBlock.objects.get(engine_block_id=vehicle.engine_block_id)
                        app_data['vehicle']['engine'] = {
                            'display': f"{block.block_type}{block.cylinders} {block.liter}L",
                            'liter': block.liter,
                            'cylinders': block.cylinders,
                            'block_type': block.block_type,
                        }
                    except:
                        pass

                # ENGINE VIN
                if vehicle.engine_vin_id:
                    try:
                        vin = EngineVIN.objects.get(engine_vin_id=vehicle.engine_vin_id)
                        app_data['vehicle']['engine_vin'] = vin.engine_vin_name
                    except:
                        pass

                # ASPIRATION
                if vehicle.aspiration_id:
                    try:
                        asp = Aspiration.objects.get(aspiration_id=vehicle.aspiration_id)
                        app_data['vehicle']['aspiration'] = asp.aspiration_name
                    except:
                        pass

                # TRANSMISSION BASE
                if vehicle.transmission_base_id:
                    try:
                        trans = TransmissionBase.objects.select_related(
                            'transmission_type',
                            'transmission_num_speeds',
                            'transmission_control_type'
                        ).get(transmission_base_id=vehicle.transmission_base_id)
                        app_data['vehicle']['transmission'] = {
                            'display': f"{trans.transmission_num_speeds.transmission_num_speeds}-Speed {trans.transmission_type.transmission_type_name}",
                            'type': trans.transmission_type.transmission_type_name,
                            'speeds': trans.transmission_num_speeds.transmission_num_speeds,
                            'control': trans.transmission_control_type.transmission_control_type_name,
                        }
                    except Exception:
                        app_data['vehicle']['transmission'] = {'display': f"Trans ID: {vehicle.transmission_base_id}"}

                # TRANSMISSION TYPE (fallback)
                if vehicle.transmission_type_id and 'transmission' not in app_data['vehicle']:
                    try:
                        trans_type = TransmissionType.objects.get(transmission_type_id=vehicle.transmission_type_id)
                        app_data['vehicle']['transmission'] = {
                            'display': trans_type.transmission_type_name,
                            'type': trans_type.transmission_type_name,
                        }
                    except:
                        pass

                # DRIVE TYPE
                if vehicle.drive_type_id:
                    try:
                        drive = DriveType.objects.get(drive_type_id=vehicle.drive_type_id)
                        app_data['vehicle']['drive_type'] = drive.drive_type_name
                    except:
                        pass

                # FUEL TYPE
                if vehicle.fuel_type_id:
                    try:
                        fuel = FuelType.objects.get(fuel_type_id=vehicle.fuel_type_id)
                        app_data['vehicle']['fuel_type'] = fuel.fuel_type_name
                    except:
                        pass

                # BODY TYPE
                if hasattr(vehicle, 'body_type_id') and vehicle.body_type_id:
                    try:
                        body = BodyType.objects.get(body_type_id=vehicle.body_type_id)
                        app_data['vehicle']['body_type'] = body.body_type_name
                    except:
                        pass

                # BED TYPE
                if hasattr(vehicle, 'bed_type_id') and vehicle.bed_type_id:
                    try:
                        bed = BedType.objects.get(bed_type_id=vehicle.bed_type_id)
                        app_data['vehicle']['bed_type'] = bed.bed_type_name
                    except:
                        pass

            except AcesAppVehicle.DoesNotExist:
                app_data['vehicle']['error'] = 'No vehicle record found'
            except Exception as e:
                errors.append(f"App {app.app_id} processing error: {str(e)}")
                app_data['vehicle']['error'] = f'Error: {str(e)}'

            enriched_apps.append(app_data)

        # Sorting
        if sort_by == 'year':
            enriched_apps.sort(key=lambda x: (
                x['vehicle'].get('year_from', 9999),
                x['vehicle'].get('make_obj', ''),
                x['vehicle'].get('model_obj', '')
            ))
        elif sort_by == 'make':
            enriched_apps.sort(key=lambda x: (
                x['vehicle'].get('make_obj', ''),
                x['vehicle'].get('year_from', 9999),
                x['vehicle'].get('model_obj', '')
            ))
        elif sort_by == 'model':
            enriched_apps.sort(key=lambda x: (
                x['vehicle'].get('model_obj', ''),
                x['vehicle'].get('year_from', 9999)
            ))
        else:
            enriched_apps.sort(key=lambda x: x['app'].app_id)

        summary = {
            'total_applications': total_count,
            'year_range': f"{min(year_set)}-{max(year_set)}" if year_set else 'N/A',
            'makes_count': len(make_dict),
            'models_count': len(model_dict),
            'has_qualifiers': sum(1 for app in enriched_apps if app['qualifiers']),
            'has_notes': sum(1 for app in enriched_apps if app['notes']),
        }

        paginator = Paginator(enriched_apps, 25)
        page_obj = paginator.get_page(page_num)

        context.update({
            'part_number': part_number,
            'applications': page_obj,
            'page_obj': page_obj,
            'summary': summary,
            'available_years': sorted(year_set, reverse=True),
            'available_makes': sorted(make_dict.items(), key=lambda x: x[1]),
            'available_models': sorted(model_dict.items(), key=lambda x: x[1]),
            'current_filters': {
                'year': year_filter,
                'make': make_filter,
                'model': model_filter,
                'sort': sort_by,
            },
            'debug_errors': errors if errors else None,
        })

        return render(request, 'admin/aces/part_lookup.html', context)

    # =====================================================
    # DISPLAY METHODS
    # =====================================================

    def app_id_display(self, obj):
        return format_html(
            '<strong style="color: #0066cc;">App #{}</strong>',
            obj.app_id
        )
    app_id_display.short_description = 'App ID'
    app_id_display.admin_order_field = 'app_id'

    def part_number_display(self, obj):
        return format_html(
            '<strong style="font-size: 13px;">{}</strong>',
            obj.part_number or '-'
        )
    part_number_display.short_description = 'Part Number'
    part_number_display.admin_order_field = 'part_number'

    def part_type_display(self, obj):
        # TODO: Link to PCdb PartType when available
        return f"Type {obj.part_type_id}" if obj.part_type_id else '-'
    part_type_display.short_description = 'Part Type'

    def vehicle_summary(self, obj):
        """Quick summary of vehicle for list view"""
        try:
            vehicle = obj.acesappvehicle
            if vehicle.base_vehicle:
                return vehicle.base_vehicle.get_display_name()
            elif vehicle.year_from and vehicle.make:
                make = vehicle.make
                year_str = f"{vehicle.year_from}"
                if vehicle.year_to and vehicle.year_to != vehicle.year_from:
                    year_str += f"-{vehicle.year_to}"
                return f"{year_str} {make}"
            return "See details"
        except:
            return '-'
    vehicle_summary.short_description = 'Vehicle'

    def vehicle_summary_full(self, obj):
        """Full vehicle description for detail view"""
        try:
            vehicle = obj.acesappvehicle
            parts = []

            if vehicle.base_vehicle_id if vehicle.base_vehicle else None:
                try:
                    bv = BaseVehicle.objects.get(base_vehicle_id=vehicle.base_vehicle_id if vehicle.base_vehicle else None)
                    parts.append(format_html(
                        '<div style="font-size: 16px; font-weight: bold; color: #0066cc; margin-bottom: 10px;">{}</div>',
                        bv.get_display_name()
                    ))
                except:
                    parts.append(f"Base Vehicle ID: {vehicle.base_vehicle_id if vehicle.base_vehicle else None}")

            if vehicle.submodel:
                try:
                    submodel = SubModel.objects.get(submodel_id=vehicle.submodel)
                    parts.append(f"SubModel: {submodel}")
                except:
                    pass

            if vehicle.engine_base_id:
                try:
                    eng = EngineBase.objects.get(engine_base_id=vehicle.engine_base_id)
                    parts.append(f"Engine: {eng}")
                except:
                    pass

            if parts:
                return mark_safe('<br>'.join(str(p) for p in parts))
            return '-'
        except AcesAppVehicle.DoesNotExist:
            return format_html('<span style="color: red;">No vehicle record!</span>')
    vehicle_summary_full.short_description = 'Vehicle Information'

    def qualifier_count(self, obj):
        count = obj.qualifiers.count()
        if count > 0:
            return format_html(
                '<span style="color: green; font-weight: bold;">{}</span>',
                count
            )
        return '-'
    qualifier_count.short_description = 'Qualifiers'

    def note_count(self, obj):
        count = obj.raw_attributes.filter(attr_name='note').count()
        if count > 0:
            return format_html(
                '<span style="color: blue; font-weight: bold;">{}</span>',
                count
            )
        return '-'
    note_count.short_description = 'Notes'

    def validate_display(self, obj):
        if obj.validate:
            return format_html(
                '<span style="color: green;">✓ Yes</span>'
            )
        return format_html(
            '<span style="color: red;">✗ No</span>'
        )
    validate_display.short_description = 'Validate'
    validate_display.admin_order_field = 'validate'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('acesappvehicle').prefetch_related(
            'qualifiers',
            'raw_attributes',
            'vehicle_types',
        )


# =====================================================
# REGISTER OTHER MODELS (for reference)
# =====================================================

@admin.register(AcesQualifier)
class AcesQualifierAdmin(admin.ModelAdmin):
    """Admin for viewing qualifiers separately"""
    list_display = ('app', 'qual_id', 'qual_text', 'param_1')
    list_filter = ('qual_id',)
    search_fields = ('qual_text', 'param_1', 'param_2', 'param_3')
    readonly_fields = ('app', 'qual_id', 'qual_text', 'param_1', 'param_2', 'param_3')


@admin.register(AcesRawAttribute)
class AcesRawAttributeAdmin(admin.ModelAdmin):
    """Admin for viewing raw attributes"""
    list_display = ('app', 'attr_name', 'attr_id', 'attr_value_short', 'idx')
    list_filter = ('attr_name',)
    search_fields = ('attr_name', 'attr_value')
    readonly_fields = ('app', 'attr_name', 'attr_id', 'attr_value', 'idx')

    def attr_value_short(self, obj):
        if obj.attr_value:
            return obj.attr_value[:100] + '...' if len(obj.attr_value) > 100 else obj.attr_value
        return '-'
    attr_value_short.short_description = 'Value'