"""Views for the exports application."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def export_list(request):
    """List user's export jobs."""
    return render(request, 'exports/export_list.html')

@login_required
def export_form(request):
    """Create new export."""
    return render(request, 'exports/export_form.html')
