"""
URL Configuration for AutoCare Application.

This module defines URL patterns for accessing AutoCare data via API endpoints.
These are example endpoints that can be customized for your needs.
"""
from django.urls import path
from . import views

app_name = 'autocare'

urlpatterns = [
    # Vehicle endpoints
    path('makes/', views.get_makes, name='makes'),
    path('years/', views.get_years, name='years'),
    path('makes/<int:make_id>/models/', views.get_models_by_make, name='models-by-make'),
    path('vehicles/', views.get_vehicles, name='vehicles'),
    path('vehicles/<int:vehicle_id>/', views.get_vehicle_detail, name='vehicle-detail'),
    
    # Parts endpoints
    path('parts/', views.get_parts, name='parts'),
    path('categories/', views.get_categories, name='categories'),
    
    # Qualifier endpoints
    path('qualifiers/', views.get_qualifiers, name='qualifiers'),
]

"""
To include these URLs in your main project, add to your project's urls.py:

from django.urls import path, include

urlpatterns = [
    # ... other patterns
    path('api/autocare/', include('autocare.urls')),
]

This will make the endpoints available at:
- /api/autocare/makes/
- /api/autocare/years/
- /api/autocare/vehicles/
- etc.
"""
