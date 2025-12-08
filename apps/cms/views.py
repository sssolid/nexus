"""
Views for static pages (Terms of Service, Privacy Policy, Contact).
"""
from django.shortcuts import render


def terms_of_service(request):
    """Display Terms of Service page."""
    return render(request, 'pages/terms.html')


def privacy_policy(request):
    """Display Privacy Policy page."""
    return render(request, 'pages/privacy.html')


def contact_us(request):
    """Display Contact Us page."""
    return render(request, 'pages/contact.html')