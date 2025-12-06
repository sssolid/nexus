"""
ASGI config for nexus project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# Read from environment, fallback to development in Docker, production otherwise
settings_module = os.environ.get(
    'DJANGO_SETTINGS_MODULE',
    'config.settings.development'  # Default for Docker
)
os.environ['DJANGO_SETTINGS_MODULE'] = settings_module

application = get_asgi_application()
