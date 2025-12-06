#!/bin/bash
# Script to create __init__.py and apps.py files for all apps

# Products app
cat > /home/claude/nexus/apps/products/__init__.py << 'EOF'
"""
Products application for product catalog management.
"""
default_app_config = 'apps.products.apps.ProductsConfig'
EOF

cat > /home/claude/nexus/apps/products/apps.py << 'EOF'
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
EOF

# ACES/PIES app
cat > /home/claude/nexus/apps/aces_pies/__init__.py << 'EOF'
"""
ACES/PIES application for automotive fitment data.
"""
default_app_config = 'apps.aces_pies.apps.AcesPiesConfig'
EOF

cat > /home/claude/nexus/apps/aces_pies/apps.py << 'EOF'
"""
ACES/PIES application configuration.
"""
from django.apps import AppConfig


class AcesPiesConfig(AppConfig):
    """Configuration for the ACES/PIES application."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.aces_pies'
    verbose_name = 'ACES & PIES Data'
EOF

# Pricing app
cat > /home/claude/nexus/apps/pricing/__init__.py << 'EOF'
"""
Pricing application for customer-specific pricing management.
"""
default_app_config = 'apps.pricing.apps.PricingConfig'
EOF

cat > /home/claude/nexus/apps/pricing/apps.py << 'EOF'
"""
Pricing application configuration.
"""
from django.apps import AppConfig


class PricingConfig(AppConfig):
    """Configuration for the pricing application."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.pricing'
    verbose_name = 'Pricing Management'
EOF

# Exports app
cat > /home/claude/nexus/apps/exports/__init__.py << 'EOF'
"""
Exports application for data export and delivery.
"""
default_app_config = 'apps.exports.apps.ExportsConfig'
EOF

cat > /home/claude/nexus/apps/exports/apps.py << 'EOF'
"""
Exports application configuration.
"""
from django.apps import AppConfig


class ExportsConfig(AppConfig):
    """Configuration for the exports application."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.exports'
    verbose_name = 'Data Exports'
EOF

# Validator app
cat > /home/claude/nexus/apps/validator/__init__.py << 'EOF'
"""
Validator application for product data validation.
"""
default_app_config = 'apps.validator.apps.ValidatorConfig'
EOF

cat > /home/claude/nexus/apps/validator/apps.py << 'EOF'
"""
Validator application configuration.
"""
from django.apps import AppConfig


class ValidatorConfig(AppConfig):
    """Configuration for the validator application."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.validator'
    verbose_name = 'Data Validator'
EOF

# Data Sync app
cat > /home/claude/nexus/apps/data_sync/__init__.py << 'EOF'
"""
Data Sync application for FileMaker synchronization.
"""
default_app_config = 'apps.data_sync.apps.DataSyncConfig'
EOF

cat > /home/claude/nexus/apps/data_sync/apps.py << 'EOF'
"""
Data Sync application configuration.
"""
from django.apps import AppConfig


class DataSyncConfig(AppConfig):
    """Configuration for the data sync application."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.data_sync'
    verbose_name = 'FileMaker Sync'
EOF

# Media Library app
cat > /home/claude/nexus/apps/media_library/__init__.py << 'EOF'
"""
Media Library application for product media management.
"""
default_app_config = 'apps.media_library.apps.MediaLibraryConfig'
EOF

cat > /home/claude/nexus/apps/media_library/apps.py << 'EOF'
"""
Media Library application configuration.
"""
from django.apps import AppConfig


class MediaLibraryConfig(AppConfig):
    """Configuration for the media library application."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.media_library'
    verbose_name = 'Media Library'
EOF

# API app
cat > /home/claude/nexus/apps/api/__init__.py << 'EOF'
"""
API application for REST API endpoints.
"""
default_app_config = 'apps.api.apps.ApiConfig'
EOF

cat > /home/claude/nexus/apps/api/apps.py << 'EOF'
"""
API application configuration.
"""
from django.apps import AppConfig


class ApiConfig(AppConfig):
    """Configuration for the API application."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.api'
    verbose_name = 'REST API'
EOF

echo "All app configuration files created successfully!"
