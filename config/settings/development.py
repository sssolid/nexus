"""
Development settings for Crown Nexus System.
"""

import sys
from .base import *

# ============================================================
# Detect management commands
# ============================================================

IS_MANAGEMENT_COMMAND = any(
    cmd in sys.argv
    for cmd in (
        "makemigrations",
        "migrate",
        "collectstatic",
        "createsuperuser",
        "shell",
    )
)

# ============================================================
# Core dev flags
# ============================================================

DEBUG = True

ALLOWED_HOSTS = [
    "*",
]

INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
]

print("#" * 50)
print("# DEVELOPMENT MODE ACTIVE")
print("#" * 50)

# ============================================================
# Development-only apps (ALWAYS INSTALLED)
# ============================================================

INSTALLED_APPS += [
    "debug_toolbar",
    "django_extensions",
    "silk",
]

# ============================================================
# Development-only middleware (REQUEST PATH ONLY)
# ============================================================

if not IS_MANAGEMENT_COMMAND:
    auth_index = MIDDLEWARE.index(
        "django.contrib.auth.middleware.AuthenticationMiddleware"
    )

    MIDDLEWARE.insert(
        auth_index + 1,
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    )

    MIDDLEWARE.append(
        "silk.middleware.SilkyMiddleware",
    )

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME", default="nexus"),
        "USER": env("DB_USER", default="postgres"),
        "PASSWORD": env("DB_PASSWORD", default="postgres"),
        "HOST": env("DB_HOST", default="localhost"),
        "PORT": env("DB_PORT", default="5432"),
        "ATOMIC_REQUESTS": True,
        "CONN_MAX_AGE": 600,
        "OPTIONS": {
            "connect_timeout": 10,
            "options": "-c search_path=public,staging",
        },
    },
    "mysql_autocare_vcdb": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "mysql_autocare_vcdb",
        "USER": "root",
        "PASSWORD": "root",
        "HOST": "mysql-inspector",
        "PORT": "3306",
    },
    "mysql_autocare_pcdb": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "mysql_autocare_pcdb",
        "USER": "root",
        "PASSWORD": "root",
        "HOST": "mysql-inspector",
        "PORT": "3306",
    },
    "mysql_autocare_pcadb": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "mysql_autocare_pcadb",
        "USER": "root",
        "PASSWORD": "root",
        "HOST": "mysql-inspector",
        "PORT": "3306",
    },
}

# ============================================================
# Debug Toolbar
# ============================================================

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG,
    "SHOW_TEMPLATE_CONTEXT": True,
}

# ============================================================
# Silk
# ============================================================

SILKY_PYTHON_PROFILER = True
SILKY_PYTHON_PROFILER_BINARY = True
SILKY_AUTHENTICATION = True
SILKY_AUTHORISATION = True
SILKY_MAX_REQUEST_BODY_SIZE = -1
SILKY_MAX_RESPONSE_BODY_SIZE = 1024

# ============================================================
# Security relaxations (dev only)
# ============================================================

SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

SECURE_BROWSER_XSS_FILTER = False
SECURE_CONTENT_TYPE_NOSNIFF = False

CONTENT_SECURITY_POLICY["DIRECTIVES"]["frame-ancestors"] = ("'self'",)
CONTENT_SECURITY_POLICY["DIRECTIVES"]["connect-src"] += ("ws:", "http:")
CONTENT_SECURITY_POLICY["DIRECTIVES"]["style-src"] += (
    "https://cdn.jsdelivr.net",
    "https://cdnjs.cloudflare.com",
)

CONTENT_SECURITY_POLICY["DIRECTIVES"]["font-src"] += (
    "https://cdnjs.cloudflare.com",
)

CONTENT_SECURITY_POLICY["DIRECTIVES"]["script-src"] += (
    "https://cdn.jsdelivr.net",
    "https://unpkg.com",
)
CONTENT_SECURITY_POLICY["DIRECTIVES"]["img-src"] += (
    'self',
    "data:",
    "https://crownautomotive.net",
    "https://mcusercontent.com",
    "http://www.gravatar.com",
    "https://www.gravatar.com",
    # Mailchimp image hosting
    "https://*.mailchimp.com",
    "https://*.mailchimpusercontent.com",
    "https://gallery.mailchimp.com",
    "https://*.mcusercontent.com",
)

AXES_ENABLED = False

# ============================================================
# Axes (more forgiving)
# ============================================================

AXES_FAILURE_LIMIT = 10
AXES_COOLOFF_TIME = 0.25
AXES_RESET_ON_SUCCESS = True

# ============================================================
# Password validation (lighter)
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 8},
    }
]

# ============================================================
# Verbose logging
# ============================================================

LOGGING["loggers"] = {
    "django.db.backends": {
        "handlers": ["console"],
        "level": "WARNING",
        "propagate": False,
    },
    "django.request": {
        "handlers": ["console"],
        "level": "DEBUG",
        "propagate": False,
    },
}

# ============================================================
# Disable cached templates
# ============================================================

TEMPLATES[0]["APP_DIRS"] = False
TEMPLATES[0]["OPTIONS"]["loaders"] = [
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
]