"""
Pricing application configuration.
"""
from django.apps import AppConfig


class PricingConfig(AppConfig):
    """Configuration for the pricing application."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.pricing'
    verbose_name = 'Pricing Management'
