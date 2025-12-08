"""
CMS application configuration.
"""
from django.apps import AppConfig


class CmsConfig(AppConfig):
    """Configuration for the CMS application."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.cms'
    verbose_name = 'CMS & Content'
