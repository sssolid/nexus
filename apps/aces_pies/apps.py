"""
ACES/PIES application configuration.
"""
from django.apps import AppConfig


class AcesPiesConfig(AppConfig):
    """Configuration for the ACES/PIES application."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.aces_pies'
    verbose_name = 'ACES & PIES Data'
