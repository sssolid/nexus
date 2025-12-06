"""Views for the validator application."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def validator_upload(request):
    """Upload file for validation."""
    return render(request, 'validator/upload_form.html')
