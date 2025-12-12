"""
Production settings for Crown Nexus System.

These settings are used in production deployment.
"""

import os

import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration

from .base import *  # noqa

print("=" * 50)
print("PRODUCTION MODE ACTIVE")
print("=" * 50)

# ============================================================
# Core
# ============================================================

DEBUG = False

# Prefer explicit hosts from .env.production
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

# ============================================================
# Security (HTTPS, HSTS, cookies)
# ============================================================

# If behind a reverse proxy (nginx/traefik), this is typical:
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=True)

SESSION_COOKIE_SECURE = env.bool("SESSION_COOKIE_SECURE", default=True)
CSRF_COOKIE_SECURE = env.bool("CSRF_COOKIE_SECURE", default=True)

SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=31536000)  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_REFERRER_POLICY = "same-origin"

X_FRAME_OPTIONS = "DENY"

# CSRF hardening
CSRF_USE_SESSIONS = True
CSRF_COOKIE_SAMESITE = "Strict"

# Session cookie hardening (keep base default unless you explicitly want Strict)
SESSION_COOKIE_SAMESITE = "Lax"

# ============================================================
# Admin URL hardening (optional)
# Use ADMIN_URL in .env.production to move admin off /admin/
# ============================================================

ADMIN_URL = env("ADMIN_URL", default="admin/")

# ============================================================
# Axes (production)
# ============================================================

AXES_FAILURE_LIMIT = env.int("AXES_FAILURE_LIMIT", default=5)
AXES_COOLOFF_TIME = env.float("AXES_COOLOFF_TIME", default=1.0)  # hours
AXES_RESET_ON_SUCCESS = True

# ============================================================
# Database
# ============================================================

DATABASES["default"]["CONN_MAX_AGE"] = 600
DATABASES["default"]["CONN_HEALTH_CHECKS"] = True

# ============================================================
# Cache timeouts (production)
# ============================================================

CACHES["default"]["TIMEOUT"] = 900  # 15 minutes

# ============================================================
# Celery (production)
# ============================================================

CELERY_TASK_ALWAYS_EAGER = False
CELERY_TASK_EAGER_PROPAGATES = False
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# ============================================================
# Email (production)
# ============================================================

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# ============================================================
# Rate limiting feature flag (views must still apply decorators)
# ============================================================

RATELIMIT_ENABLE = env.bool("RATELIMIT_ENABLE", default=True)

# ============================================================
# Wagtail
# ============================================================

WAGTAILADMIN_BASE_URL = env(
    "WAGTAILADMIN_BASE_URL",
    default=SITE_URL,
)

# ============================================================
# Static/Media storage (S3 optional)
# Requires: django-storages + boto3 and correct bucket permissions
# ============================================================

if env.bool("USE_S3", default=False):
    # These must be set in .env.production if USE_S3=True
    AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME", default="us-east-1")

    # Optional: custom domain; default AWS endpoint if not set
    AWS_S3_CUSTOM_DOMAIN = env(
        "AWS_S3_CUSTOM_DOMAIN",
        default=f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com",
    )

    AWS_S3_OBJECT_PARAMETERS = {
        "CacheControl": "max-age=86400",
    }

    # Recommended defaults
    AWS_DEFAULT_ACL = None
    AWS_QUERYSTRING_AUTH = False

    # NOTE:
    # Using S3 for BOTH static and media is common, but many deployments keep
    # static on the app and only media in S3. This keeps your current behavior:
    # - static on S3
    # - media on S3
    STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"

# ============================================================
# Sentry (optional)
# ============================================================

SENTRY_DSN = env("SENTRY_DSN", default="")
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            DjangoIntegration(),
            CeleryIntegration(),
            RedisIntegration(),
        ],
        traces_sample_rate=0.1,
        send_default_pii=False,
        environment="production",
    )

# ============================================================
# Logging (production)
# File logging path should be a mounted volume in containers
# ============================================================

LOG_DIR = "/var/log/django"
os.makedirs(LOG_DIR, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": f"{LOG_DIR}/django.log",
            "maxBytes": 1024 * 1024 * 15,  # 15MB
            "backupCount": 10,
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "WARNING",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console", "file"],
            "level": "ERROR",
            "propagate": False,
        },
        "celery": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
