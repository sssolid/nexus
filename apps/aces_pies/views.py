"""Views for the ACES/PIES application."""
from django.shortcuts import render

def vehicle_search(request):
    """Search products by vehicle."""
    return render(request, 'aces_pies/vehicle_search.html')
