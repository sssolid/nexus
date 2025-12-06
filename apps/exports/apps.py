"""
Exports application configuration.
"""
from django.apps import AppConfig


class ExportsConfig(AppConfig):
    """Configuration for the exports application."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.exports'
    verbose_name = 'Data Exports'
