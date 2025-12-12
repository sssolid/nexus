"""
Accounts application configuration.
"""
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Configuration for the accounts application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"
    verbose_name = "User Accounts"

    def ready(self):
        """Import signals/audit registrations when app is ready."""
        from . import signals  # noqa
        from . import audit_otp  # noqa
