"""
Celery configuration for asynchronous task processing.
"""
import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# Set the default Django settings module
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    os.getenv("DJANGO_SETTINGS_MODULE", "config.settings.base")
)

app = Celery("nexus")

app.conf.enable_utc = True
app.conf.timezone = "America/New_York"

# Load configuration from Django settings
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# ---------------------------------------------------------------------
# Beat schedule
# ---------------------------------------------------------------------
# IMPORTANT:
# - This ONLY triggers the task periodically
# - It does NOT mean a sync will actually run
# - The task itself decides if a sync is due
# ---------------------------------------------------------------------
app.conf.beat_schedule = {
    "sync-filemaker-check-every-5-min": {
        "task": "apps.data_sync.tasks.sync_filemaker_data",
        "schedule": crontab(minute="*/1"),
    },

    "process-scheduled-exports-every-15-min": {
        "task": "apps.exports.tasks.process_scheduled_exports",
        "schedule": crontab(minute="*/15"),
    },

    "cleanup-old-export-files-daily": {
        "task": "apps.exports.tasks.cleanup_old_exports",
        "schedule": crontab(hour=2, minute=0),
    },

    "update-product-search-index-nightly": {
        "task": "apps.products.tasks.update_search_index",
        "schedule": crontab(hour=1, minute=0),
    },

    "generate-aces-pies-materialized-views": {
        "task": "apps.aces_pies.tasks.refresh_materialized_views",
        "schedule": crontab(hour=3, minute=0),
    },
}


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
