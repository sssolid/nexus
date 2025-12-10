"""
AutoCare Django Application Configuration.

This app manages the Auto Care Association standard databases:
- VCdb (Vehicle Component Database)
- Qdb (Qualifier Database)
- PCdb (Product Component Database)
- PAdb (Part Attribute Database)
"""
from django.apps import AppConfig


class AutocareConfig(AppConfig):
    """Configuration for the AutoCare application."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.autocare'
    verbose_name = 'Auto Care Standards'

    def ready(self):
        """Import signals and perform other initialization."""
        pass
