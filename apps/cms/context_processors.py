"""
Context processors for Crown Nexus.

Makes common data available in all templates.
"""

from django.core.cache import cache

from apps.products.models import ProductCategory


def site_context(request):
    """
    Add common site data to all template contexts.
    """
    context = {}

    # Get cached categories for navigation
    categories = cache.get("nav_categories")
    if categories is None:
        categories = ProductCategory.objects.filter(is_active=True, parent=None)[:6]
        cache.set("nav_categories", categories, timeout=7200)

    context["nav_categories"] = categories

    # Add user role helpers
    if request.user.is_authenticated:
        context["is_customer"] = request.user.is_customer
        context["is_employee"] = request.user.is_employee

    return context


def cached_stats(request):
    """
    Add cached statistics to template context.
    """
    stats = cache.get("product_stats")
    if stats:
        return {"product_stats": stats}
    return {}
