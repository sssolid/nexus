"""
Products application configuration.
"""
from django.apps import AppConfig


class ProductsConfig(AppConfig):
    """Configuration for the products application."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.products'
    verbose_name = 'Product Catalog'
    
    def ready(self):
        """Import signals when app is ready."""
        import apps.products.signals  # noqa
