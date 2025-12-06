"""
Data Sync application configuration.
"""
from django.apps import AppConfig


class DataSyncConfig(AppConfig):
    """Configuration for the data sync application."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.data_sync'
    verbose_name = 'FileMaker Sync'
