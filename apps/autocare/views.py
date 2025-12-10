"""
Views for AutoCare Application.

This module provides example views for accessing AutoCare data.
These can be used as templates for creating your own API endpoints.
"""
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q, Prefetch

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


@require_http_methods(["GET"])
def get_makes(request):
    """
    Get list of vehicle makes.
    
    Query Parameters:
        search: Filter makes by name (optional)
        page: Page number for pagination (default: 1)
        per_page: Items per page (default: 20, max: 100)
    
    Returns:
        JSON response with list of makes
    """
    search = request.GET.get('search', '')
    page = int(request.GET.get('page', 1))
    per_page = min(int(request.GET.get('per_page', 20)), 100)
    
    # Query makes
    makes = Make.objects.all().order_by('make_name')
    
    if search:
        makes = makes.filter(make_name__icontains=search)
    
    # Paginate
    paginator = Paginator(makes, per_page)
    page_obj = paginator.get_page(page)
    
    data = {
        'count': paginator.count,
        'num_pages': paginator.num_pages,
        'current_page': page,
        'results': [
            {
                'make_id': make.make_id,
                'make_name': make.make_name,
            }
            for make in page_obj
        ]
    }
    
    return JsonResponse(data)


@require_http_methods(["GET"])
def get_years(request):
    """
    Get list of vehicle years.
    
    Returns:
        JSON response with list of years
    """
    years = Year.objects.all().order_by('-year_id')
    
    data = {
        'count': years.count(),
        'results': [
            {'year_id': year.year_id}
            for year in years
        ]
    }
    
    return JsonResponse(data)


@require_http_methods(["GET"])
def get_models_by_make(request, make_id):
    """
    Get list of models for a specific make.
    
    Args:
        make_id: The make ID to filter by
    
    Query Parameters:
        year: Filter by year (optional)
    
    Returns:
        JSON response with list of models
    """
    year_id = request.GET.get('year')
    
    # Get base vehicles for this make
    base_vehicles = BaseVehicle.objects.filter(make_id=make_id)
    
    if year_id:
        base_vehicles = base_vehicles.filter(year_id=year_id)
    
    # Get unique models
    models = Model.objects.filter(
        base_vehicles__in=base_vehicles
    ).distinct().order_by('model_name')
    
    data = {
        'make_id': make_id,
        'count': models.count(),
        'results': [
            {
                'model_id': model.model_id,
                'model_name': model.model_name,
                'vehicle_type': {
                    'id': model.vehicle_type.vehicle_type_id,
                    'name': model.vehicle_type.vehicle_type_name,
                } if model.vehicle_type else None,
            }
            for model in models.select_related('vehicle_type')
        ]
    }
    
    return JsonResponse(data)


@require_http_methods(["GET"])
def get_vehicles(request):
    """
    Get list of vehicles with filtering.
    
    Query Parameters:
        make_id: Filter by make ID (optional)
        year_id: Filter by year ID (optional)
        model_id: Filter by model ID (optional)
        page: Page number for pagination (default: 1)
        per_page: Items per page (default: 20, max: 100)
    
    Returns:
        JSON response with list of vehicles
    """
    # Get filter parameters
    make_id = request.GET.get('make_id')
    year_id = request.GET.get('year_id')
    model_id = request.GET.get('model_id')
    page = int(request.GET.get('page', 1))
    per_page = min(int(request.GET.get('per_page', 20)), 100)
    
    # Build query
    vehicles = Vehicle.objects.select_related(
        'base_vehicle__make',
        'base_vehicle__year',
        'base_vehicle__model',
        'sub_model',
        'region'
    )
    
    # Apply filters
    if make_id:
        vehicles = vehicles.filter(base_vehicle__make_id=make_id)
    if year_id:
        vehicles = vehicles.filter(base_vehicle__year_id=year_id)
    if model_id:
        vehicles = vehicles.filter(base_vehicle__model_id=model_id)
    
    # Paginate
    paginator = Paginator(vehicles, per_page)
    page_obj = paginator.get_page(page)
    
    data = {
        'count': paginator.count,
        'num_pages': paginator.num_pages,
        'current_page': page,
        'results': [
            {
                'vehicle_id': vehicle.vehicle_id,
                'year': vehicle.base_vehicle.year.year_id,
                'make': {
                    'id': vehicle.base_vehicle.make.make_id,
                    'name': vehicle.base_vehicle.make.make_name,
                },
                'model': {
                    'id': vehicle.base_vehicle.model.model_id,
                    'name': vehicle.base_vehicle.model.model_name,
                },
                'sub_model': {
                    'id': vehicle.sub_model.sub_model_id,
                    'name': vehicle.sub_model.sub_model_name,
                },
                'region': {
                    'id': vehicle.region.region_id,
                    'name': vehicle.region.region_name,
                },
            }
            for vehicle in page_obj
        ]
    }
    
    return JsonResponse(data)


@require_http_methods(["GET"])
def get_vehicle_detail(request, vehicle_id):
    """
    Get detailed information for a specific vehicle.
    
    Args:
        vehicle_id: The vehicle ID
    
    Returns:
        JSON response with vehicle details including configurations
    """
    try:
        vehicle = Vehicle.objects.select_related(
            'base_vehicle__make',
            'base_vehicle__year',
            'base_vehicle__model',
            'sub_model',
            'region'
        ).prefetch_related(
            'drive_types',
            'engine_configs__engine_block',
            'transmissions__transmission_base__transmission_type',
        ).get(vehicle_id=vehicle_id)
    except Vehicle.DoesNotExist:
        return JsonResponse({'error': 'Vehicle not found'}, status=404)
    
    data = {
        'vehicle_id': vehicle.vehicle_id,
        'year': vehicle.base_vehicle.year.year_id,
        'make': {
            'id': vehicle.base_vehicle.make.make_id,
            'name': vehicle.base_vehicle.make.make_name,
        },
        'model': {
            'id': vehicle.base_vehicle.model.model_id,
            'name': vehicle.base_vehicle.model.model_name,
        },
        'sub_model': {
            'id': vehicle.sub_model.sub_model_id,
            'name': vehicle.sub_model.sub_model_name,
        },
        'region': {
            'id': vehicle.region.region_id,
            'name': vehicle.region.region_name,
        },
        'drive_types': [
            {
                'id': dt.drive_type_id,
                'name': dt.drive_type_name,
            }
            for dt in vehicle.drive_types.all()
        ],
        'engine_configs': [
            {
                'id': ec.engine_config_id,
                'liter': ec.engine_block.liter,
                'cylinders': ec.engine_block.cylinders,
            }
            for ec in vehicle.engine_configs.all()
        ],
        'transmissions': [
            {
                'id': t.transmission_id,
                'type': t.transmission_base.transmission_type.transmission_type_name,
            }
            for t in vehicle.transmissions.all()
        ],
    }
    
    return JsonResponse(data)


@require_http_methods(["GET"])
def get_parts(request):
    """
    Get list of parts with filtering.
    
    Query Parameters:
        search: Filter parts by name (optional)
        category_id: Filter by category ID (optional)
        page: Page number for pagination (default: 1)
        per_page: Items per page (default: 20, max: 100)
    
    Returns:
        JSON response with list of parts
    """
    search = request.GET.get('search', '')
    category_id = request.GET.get('category_id')
    page = int(request.GET.get('page', 1))
    per_page = min(int(request.GET.get('per_page', 20)), 100)
    
    # Build query
    parts = Parts.objects.select_related('parts_description')
    
    if search:
        parts = parts.filter(part_terminology_name__icontains=search)
    
    if category_id:
        parts = parts.filter(categories__category_id=category_id)
    
    # Paginate
    paginator = Paginator(parts.distinct(), per_page)
    page_obj = paginator.get_page(page)
    
    data = {
        'count': paginator.count,
        'num_pages': paginator.num_pages,
        'current_page': page,
        'results': [
            {
                'part_terminology_id': part.part_terminology_id,
                'part_terminology_name': part.part_terminology_name,
                'description': part.parts_description.parts_description if part.parts_description else None,
            }
            for part in page_obj
        ]
    }
    
    return JsonResponse(data)


@require_http_methods(["GET"])
def get_categories(request):
    """
    Get list of part categories.
    
    Returns:
        JSON response with list of categories
    """
    categories = Category.objects.all().order_by('category_name')
    
    data = {
        'count': categories.count(),
        'results': [
            {
                'category_id': cat.category_id,
                'category_name': cat.category_name,
            }
            for cat in categories
        ]
    }
    
    return JsonResponse(data)


@require_http_methods(["GET"])
def get_qualifiers(request):
    """
    Get list of qualifiers with filtering.
    
    Query Parameters:
        search: Filter qualifiers by text (optional)
        type_id: Filter by qualifier type ID (optional)
        page: Page number for pagination (default: 1)
        per_page: Items per page (default: 20, max: 100)
    
    Returns:
        JSON response with list of qualifiers
    """
    search = request.GET.get('search', '')
    type_id = request.GET.get('type_id')
    page = int(request.GET.get('page', 1))
    per_page = min(int(request.GET.get('per_page', 20)), 100)
    
    # Build query
    qualifiers = Qualifier.objects.select_related('qualifier_type')
    
    if search:
        qualifiers = qualifiers.filter(qualifier_text__icontains=search)
    
    if type_id:
        qualifiers = qualifiers.filter(qualifier_type_id=type_id)
    
    # Paginate
    paginator = Paginator(qualifiers, per_page)
    page_obj = paginator.get_page(page)
    
    data = {
        'count': paginator.count,
        'num_pages': paginator.num_pages,
        'current_page': page,
        'results': [
            {
                'qualifier_id': q.qualifier_id,
                'qualifier_text': q.qualifier_text,
                'example_text': q.example_text,
                'qualifier_type': {
                    'id': q.qualifier_type.qualifier_type_id,
                    'type': q.qualifier_type.qualifier_type,
                } if q.qualifier_type else None,
            }
            for q in page_obj
        ]
    }
    
    return JsonResponse(data)


# Add more view functions as needed for your specific use cases
