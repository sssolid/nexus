"""
Media Library application configuration.
"""
from django.apps import AppConfig


class MediaLibraryConfig(AppConfig):
    """Configuration for the media library application."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.media_library'
    verbose_name = 'Media Library'
