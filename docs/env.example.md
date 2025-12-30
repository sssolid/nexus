# Base environment (.env)

```txt
# =========================================================
# Django Core (LOCAL)
# =========================================================
DEBUG=True
SECRET_KEY=dev-local-secret-key
DJANGO_SETTINGS_MODULE=config.settings.development
SITE_URL=http://localhost:8000

ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# =========================================================
# Static / Media (LOCAL)
# =========================================================
STATIC_URL=/static/
STATIC_ROOT=staticfiles
MEDIA_URL=/media/
MEDIA_ROOT=media

# =========================================================
# Database (LOCAL – SQLite fallback)
# =========================================================
USE_SQLITE=True
SQLITE_PATH=db.sqlite3

# These exist only so settings code does not explode
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

# =========================================================
# Redis / Celery (DISABLED LOCALLY)
# =========================================================
REDIS_PASSWORD=redispassword
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_URL=redis://:redispassword@redis:6379/1

CELERY_BROKER_URL=redis://:redispassword@redis:6379/1
CELERY_RESULT_BACKEND=redis://:redispassword@redis:6379/2

# =========================================================
# Email (LOCAL)
# =========================================================
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=dev@localhost
SERVER_EMAIL=dev@localhost
SUPPORT_EMAIL=dev@localhost

EMAIL_VERIFICATION_TIMEOUT=86400
ADMIN_NOTIFICATION_EMAILS=dev@localhost

# =========================================================
# Security (LOCAL / Relaxed)
# =========================================================
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
SECURE_HSTS_SECONDS=0

# =========================================================
# FileMaker Sync (DISABLED LOCALLY)
# =========================================================
FILEMAKER_SYNC_ENABLED=False
FILEMAKER_HOST=
FILEMAKER_DATABASE=
FILEMAKER_USERNAME=
FILEMAKER_PASSWORD=
FILEMAKER_SYNC_INTERVAL=3600

# =========================================================
# AWS S3 (DISABLED)
# =========================================================
USE_S3=False
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
AWS_S3_REGION_NAME=us-east-1

# =========================================================
# SFTP (DISABLED)
# =========================================================
SFTP_ENABLED=False
SFTP_HOST=
SFTP_PORT=22
SFTP_USERNAME=
SFTP_PASSWORD=

# =========================================================
# Observability (LOCAL)
# =========================================================
SENTRY_DSN=
LOG_LEVEL=DEBUG

# =========================================================
# Rate Limiting (DISABLED)
# =========================================================
RATELIMIT_ENABLE=False
RATELIMIT_USE_CACHE=default

# =========================================================
# Uploads & Pagination
# =========================================================
MAX_UPLOAD_SIZE=104857600
DEFAULT_PAGE_SIZE=50
MAX_PAGE_SIZE=1000

# =========================
# Mailchimp
# =========================
MAILCHIMP_API_KEY=
MAILCHIMP_SERVER_PREFIX=

# =========================================================
# AutoCare (OPTIONAL / SAFE DEFAULTS)
# =========================================================
AUTOCARE_OAUTH_TOKEN_URL=
AUTOCARE_CLIENT_ID=
AUTOCARE_CLIENT_SECRET=
AUTOCARE_USERNAME=
AUTOCARE_PASSWORD=
AUTOCARE_SCOPE=

# =========================================================
# API Base URLs (OPTIONAL)
# =========================================================
VCDB_API_BASE=
```


# Override environment (.env.{development,production})

```txt
# =========================================================
# Django Core
# =========================================================
DEBUG=True
SECRET_KEY=dev-secret-key-not-for-production
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
DJANGO_SETTINGS_MODULE=config.settings.development
SITE_URL=http://localhost:8000

# =========================================================
# Static / Media
# =========================================================
STATIC_ROOT=/app/staticfiles
MEDIA_ROOT=/app/media

# =========================================================
# Database (Local / Docker)
# =========================================================
DB_NAME=nexus
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

# =========================================================
# PostgreSQL (container init)
# =========================================================
POSTGRES_DB=nexus
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# =========================================================
# Redis / Celery
# =========================================================
REDIS_PASSWORD=redispassword
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_URL=redis://:redispassword@redis:6379/1

CELERY_BROKER_URL=redis://:redispassword@redis:6379/1
CELERY_RESULT_BACKEND=redis://:redispassword@redis:6379/2

# =========================================================
# Email (Development Friendly)
# =========================================================
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=dev@localhost
SERVER_EMAIL=dev@localhost
SUPPORT_EMAIL=dev@localhost

EMAIL_VERIFICATION_TIMEOUT=86400
ADMIN_NOTIFICATION_EMAILS=dev@localhost

# =========================================================
# Security (Relaxed)
# =========================================================
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
SECURE_HSTS_SECONDS=0

# =========================================================
# FileMaker Sync (Optional)
# =========================================================
FILEMAKER_HOST=filemaker-server.local
FILEMAKER_DATABASE=
FILEMAKER_USERNAME=
FILEMAKER_PASSWORD=
FILEMAKER_SYNC_ENABLED=False
FILEMAKER_SYNC_INTERVAL=3600

# =========================================================
# AWS S3 (Disabled)
# =========================================================
USE_S3=False
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
AWS_S3_REGION_NAME=us-east-1

# =========================================================
# SFTP (Disabled)
# =========================================================
SFTP_ENABLED=False
SFTP_HOST=
SFTP_PORT=22
SFTP_USERNAME=
SFTP_PASSWORD=

# =========================================================
# Observability
# =========================================================
SENTRY_DSN=
LOG_LEVEL=DEBUG

# =========================================================
# Rate Limiting
# =========================================================
RATELIMIT_ENABLE=False
RATELIMIT_USE_CACHE=default

# =========================================================
# Uploads & Pagination
# =========================================================
MAX_UPLOAD_SIZE=104857600
DEFAULT_PAGE_SIZE=50
MAX_PAGE_SIZE=1000

# =========================
# Mailchimp
# =========================
MAILCHIMP_API_KEY=
MAILCHIMP_SERVER_PREFIX=us6

# =========================
# AutoCare OAuth Credentials
# =========================

AUTOCARE_OAUTH_TOKEN_URL=https://autocare-identity.autocare.org/connect/token
AUTOCARE_CLIENT_ID=
AUTOCARE_CLIENT_SECRET=
AUTOCARE_USERNAME=
AUTOCARE_PASSWORD=
AUTOCARE_SCOPE=CommonApis QDBApis PcadbApis BrandApis VcdbApis offline_access
VCDB_SWAGGER_URL=https://vcdb.autocarevip.com/swagger/v2/swagger.json
PCDB_SWAGGER_URL=https://pcdb.autocarevip.com/swagger/v2/swagger.json
QDB_SWAGGER_URL=https://qdb.autocarevip.com/swagger/v2/swagger.json

# =========================
# API Base URLs
# =========================

VCDB_API_BASE=https://vcdb.autocarevip.com/api/v1.0
VCDB_API_HOST=https://vcdb.autocarevip.com
VCDB_API_V1_BASE=https://vcdb.autocarevip.com/api/v1.0
```