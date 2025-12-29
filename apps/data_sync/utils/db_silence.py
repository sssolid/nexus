# apps/data_sync/utils/db_silence.py

from django.conf import settings

class silence_db_debug:
    def __enter__(self):
        self._old_debug = settings.DEBUG
        settings.DEBUG = False

    def __exit__(self, exc_type, exc, tb):
        from django.conf import settings
        settings.DEBUG = self._old_debug
