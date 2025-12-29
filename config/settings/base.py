"""
Base settings for Crown Nexus System.

These settings are common to all environments.
Environment-specific overrides live in development.py and production.py
"""

import os
from pathlib import Path

import environ

LOGIN_FORM_CLASS = "apps.accounts.forms.EmailAuthenticationForm"

# ============================================================
# Paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ============================================================
# Environment loading (ENV_FILE aware)
# ============================================================

env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, "django-insecure-change-this-in-production"),
    ALLOWED_HOSTS=(list, []),
)

ENV_FILE = os.environ.get("ENV_FILE", ".env")
environ.Env.read_env(os.path.join(BASE_DIR, ENV_FILE))

# ============================================================
# Core Django settings
# ============================================================

SECRET_KEY = env("SECRET_KEY")
DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS",
    default=["localhost", "127.0.0.1"],
)

SITE_URL = env("SITE_URL", default="http://localhost:8000")
WAGTAIL_SITE_NAME = "Crown Nexus"

# ============================================================
# Application definition
# ============================================================

INSTALLED_APPS = [
    # Django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",

    # REST / API
    "rest_framework",
    "rest_framework.authtoken",
    "django_filters",
    "drf_spectacular",

    # UI / UX
    "crispy_forms",
    "crispy_bootstrap5",
    "django_htmx",
    "corsheaders",

    # Background tasks
    "django_celery_beat",
    "django_celery_results",

    # Security / Auth
    "auditlog",
    "axes",
    "django_otp",
    "django_otp.plugins.otp_totp",
    "django_otp.plugins.otp_static",
    "two_factor",
    "django.forms",
    "csp",

    # Permissions
    "guardian",

    # Media
    "imagekit",
    "easy_thumbnails",
    "import_export",
    "adminsortable2",

    # Health checks
    "health_check",
    "health_check.db",
    "health_check.cache",
    "health_check.storage",

    # Wagtail
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "modelcluster",
    "taggit",

    # Countries
    "django_countries",

    # Custom apps
    "apps.core",
    "apps.common",
    "apps.cms",
    "apps.accounts.apps.AccountsConfig",
    "apps.products",
    # "apps.autocare",
    "apps.autocare.aces.apps.AutocareACESConfig",
    "apps.autocare.core.apps.AutocareCoreConfig",
    "apps.autocare.pies.apps.AutocarePIESConfig",
    # "apps.autocare.models.reference.apps.AutocareReferenceConfig",
    "apps.autocare.vcdb.apps.AutocareVCDBConfig",
    "apps.autocare.pcdb.apps.AutocarePCDBConfig",
    "apps.autocare.padb.apps.AutocarePADBConfig",
    "apps.autocare.qdb.apps.AutocareQDBConfig",
    "apps.aces_pies",
    "apps.pricing",
    "apps.media_library",
    "apps.exports",
    "apps.data_sync",
    "apps.validator",
    "apps.api",
]

# ============================================================
# Middleware (ORDER MATTERS)
# ============================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    "csp.middleware.CSPMiddleware",

    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",

    # Authentication (ONCE)
    "django.contrib.auth.middleware.AuthenticationMiddleware",

    # Timezone Activation
    "apps.accounts.middleware.UserTimezoneMiddleware",

    # OTP must follow auth
    "django_otp.middleware.OTPMiddleware",

    # Enforce 2FA
    "apps.accounts.middleware.Enforce2FAMiddleware",

    # Brute-force protection
    "axes.middleware.AxesMiddleware",

    # HTMX
    "django_htmx.middleware.HtmxMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    # Wagtail redirects last
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

# ============================================================
# URLs / Templates
# ============================================================

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "apps.cms.context_processors.site_context",
                "apps.cms.context_processors.cached_stats",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ============================================================
# Crispy Forms
# ============================================================

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# ============================================================
# Database
# ============================================================

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
        },
    },
}

# ============================================================
# Authentication
# ============================================================

AUTH_USER_MODEL = "accounts.User"

AUTHENTICATION_BACKENDS = [
    # 1. Security / lockout (must be first)
    "axes.backends.AxesBackend",

    # 2. Your custom gate (verified + approved)
    "apps.accounts.auth_backends.VerifiedApprovedBackend",

    # 3. Django’s core permission system (REQUIRED)
    "django.contrib.auth.backends.ModelBackend",

    # 4. Object-level permissions (optional, last)
    "guardian.backends.ObjectPermissionBackend",
]

LOGIN_URL = "two_factor:login"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "two_factor:login"
WAGTAILADMIN_BASE_URL = SITE_URL.rstrip("/") + "/cms/"
TWO_FACTOR_LOGIN_TIMEOUT = 300

# ============================================================
# Passwords
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 10},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

# ============================================================
# Sessions / Cookies
# ============================================================

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
SESSION_COOKIE_AGE = 86400
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = "Lax"

# ============================================================
# Internationalization
# ============================================================

LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/New_York"
USE_I18N = True
USE_TZ = True

# ============================================================
# Static / Media
# ============================================================

STATIC_URL = "/static/"
STATIC_ROOT = env("STATIC_ROOT", default=BASE_DIR / "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

MEDIA_URL = "/media/"
MEDIA_ROOT = env("MEDIA_ROOT", default=BASE_DIR / "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ============================================================
# Cache (Redis)
# ============================================================

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URL", default="redis://localhost:6379/0"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": env("REDIS_PASSWORD", default=""),
        },
        "KEY_PREFIX": "nexus",
        "TIMEOUT": 300,
    }
}

# ============================================================
# Content Security Policy (django-csp >= 4.x)
# ============================================================

CONTENT_SECURITY_POLICY = {
    "DIRECTIVES": {
        "default-src": ("'self'",),
        "style-src": ("'self'", "'unsafe-inline'"),
        "script-src": ("'self'", "'unsafe-inline'"),
        "img-src": ("'self'", "data:", "blob:"),
        "font-src": ("'self'",),
        "connect-src": ("'self'",),
        "frame-ancestors": ("'none'",),
    }
}

# ============================================================
# Axes
# ============================================================

AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1
AXES_RESET_ON_SUCCESS = True

# ============================================================
# Django REST Framework
# ============================================================

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": env.int("DEFAULT_PAGE_SIZE", default=50),
    "MAX_PAGE_SIZE": env.int("MAX_PAGE_SIZE", default=1000),
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# ============================================================
# Email (baseline)
# ============================================================

EMAIL_BACKEND = env(
    "EMAIL_BACKEND",
    default="django.core.mail.backends.console.EmailBackend",
)
EMAIL_HOST = env("EMAIL_HOST", default="localhost")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = env(
    "DEFAULT_FROM_EMAIL", default="noreply@crowndataportal.com"
)
SUPPORT_EMAIL = env(
    "SUPPORT_EMAIL", default="support@crowndataportal.com"
)

EMAIL_VERIFICATION_TIMEOUT = 86400
ADMIN_NOTIFICATION_EMAILS = env.list(
    "ADMIN_NOTIFICATION_EMAILS",
    default=["support@crowndataportal.com"],
)

# ============================================================
# Auditlog
# ============================================================

AUDITLOG_LOGENTRY_MODEL = "auditlog.LogEntry"
AUDITLOG_INCLUDE_ALL_MODELS = False
AUDITLOG_DISABLE_ON_RAW_SAVE = True

# ============================================================
# FileMaker
# ============================================================

FILEMAKER_HOST=env('FILEMAKER_HOST',default='127.0.0.1')
FILEMAKER_DATABASE=env('FILEMAKER_DATABASE',default='nexus')
FILEMAKER_USERNAME=env("FILEMAKER_USERNAME",default="admin")
FILEMAKER_PASSWORD=env("FILEMAKER_PASSWORD",default="")
FILEMAKER_SYNC_ENABLED=env("FILEMAKER_SYNC_ENABLED",default=False,cast=bool)
FILEMAKER_SYNC_INTERVAL=env("FILEMAKER_SYNC_INTERVAL",default=3600,cast=int)

# ============================================================
# Mailchimp
# ============================================================
MAILCHIMP_API_KEY=env("MAILCHIMP_API_KEY",default="")
MAILCHIMP_SERVER_PREFIX=env("MAILCHIMP_SERVER_PREFIX",default="us6")

# ============================================================
# Autocare
# ============================================================

AUTOCARE_OAUTH_TOKEN_URL = env("AUTOCARE_OAUTH_TOKEN_URL", default="")
AUTOCARE_CLIENT_ID = env("AUTOCARE_CLIENT_ID", default="")
AUTOCARE_CLIENT_SECRET = env("AUTOCARE_CLIENT_SECRET", default="")
AUTOCARE_USERNAME = env("AUTOCARE_USERNAME", default="")
AUTOCARE_PASSWORD = env("AUTOCARE_PASSWORD", default="")
AUTOCARE_SCOPE = env("AUTOCARE_SCOPE", default="")

AUTOCARE_API_HOSTS = {
    "vcdb": "https://vcdb.autocarevip.com",
    "pcdb": "https://pcdb.autocarevip.com",
    "padb": "https://pcdb.autocarevip.com",
    "qdb":  "https://qdb.autocarevip.com",
    "brand":  "https://brand.autocarevip.com",
}
VCDB_API_HOST = "https://vcdb.autocarevip.com"
VCDB_API_V1_BASE = "https://vcdb.autocarevip.com/api/v1.0"
VCDB_API_BASE = env("VCDB_API_BASE")
VCDB_SWAGGER_URL = env("VCDB_SWAGGER_URL")
PCDB_SWAGGER_URL = env("PCDB_SWAGGER_URL")
QDB_SWAGGER_URL = env("QDB_SWAGGER_URL")

# ============================================================
# Logging (baseline)
# ============================================================

LOG_LEVEL = env("LOG_LEVEL", default="INFO")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": LOG_LEVEL,
    },
}
