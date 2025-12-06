"""
Validator application configuration.
"""
from django.apps import AppConfig


class ValidatorConfig(AppConfig):
    """Configuration for the validator application."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.validator'
    verbose_name = 'Data Validator'
