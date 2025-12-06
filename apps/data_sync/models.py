"""
Data Sync models for FileMaker database synchronization.

Supports:
- Scheduled synchronization from FileMaker
- Incremental and full sync
- Error tracking and retry logic
- Data transformation mapping
"""
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class SyncJob(models.Model):
    """
    Synchronization job tracking FileMaker data sync.
    """
    
    class SyncType(models.TextChoices):
        """Sync type choices."""
        FULL = 'FULL', _('Full Sync')
        INCREMENTAL = 'INCREMENTAL', _('Incremental Sync')
        MANUAL = 'MANUAL', _('Manual Sync')
    
    class SyncStatus(models.TextChoices):
        """Sync status choices."""
        PENDING = 'PENDING', _('Pending')
        RUNNING = 'RUNNING', _('Running')
        COMPLETED = 'COMPLETED', _('Completed')
        FAILED = 'FAILED', _('Failed')
        CANCELLED = 'CANCELLED', _('Cancelled')
    
    sync_type = models.CharField(
        max_length=20,
        choices=SyncType.choices,
        db_index=True
    )
    status = models.CharField(
        max_length=20,
        choices=SyncStatus.choices,
        default=SyncStatus.PENDING,
        db_index=True
    )
    
    # Sync details
    filemaker_layout = models.CharField(
        max_length=200,
        help_text=_('FileMaker layout/table name')
    )
    last_sync_timestamp = models.DateTimeField(
        blank=True,
        null=True,
        help_text=_('Timestamp from last successful sync')
    )
    
    # Statistics
    records_fetched = models.IntegerField(default=0)
    records_created = models.IntegerField(default=0)
    records_updated = models.IntegerField(default=0)
    records_failed = models.IntegerField(default=0)
    
    # Error tracking
    error_message = models.TextField(blank=True)
    error_details = models.JSONField(blank=True, null=True)
    
    # Timing
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    # Triggered by
    triggered_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='triggered_sync_jobs'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('sync job')
        verbose_name_plural = _('sync jobs')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['sync_type', 'status']),
        ]
    
    def __str__(self):
        """String representation of the sync job."""
        return f"{self.sync_type} - {self.status} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"


class SyncLog(models.Model):
    """
    Detailed log entries for sync operations.
    """
    
    class LogLevel(models.TextChoices):
        """Log level choices."""
        DEBUG = 'DEBUG', _('Debug')
        INFO = 'INFO', _('Info')
        WARNING = 'WARNING', _('Warning')
        ERROR = 'ERROR', _('Error')
    
    sync_job = models.ForeignKey(
        SyncJob,
        on_delete=models.CASCADE,
        related_name='logs'
    )
    
    level = models.CharField(
        max_length=20,
        choices=LogLevel.choices,
        default=LogLevel.INFO,
        db_index=True
    )
    message = models.TextField()
    details = models.JSONField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        verbose_name = _('sync log')
        verbose_name_plural = _('sync logs')
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['sync_job', 'level']),
        ]
    
    def __str__(self):
        """String representation of the sync log."""
        return f"[{self.level}] {self.message[:50]}"


class DataMapping(models.Model):
    """
    Field mapping between FileMaker and Django models.
    """
    
    class TargetModel(models.TextChoices):
        """Target Django model choices."""
        PRODUCT = 'PRODUCT', _('Product')
        CATEGORY = 'CATEGORY', _('Product Category')
        MANUFACTURER = 'MANUFACTURER', _('Manufacturer')
        ATTRIBUTES = 'ATTRIBUTES', _('Product Attributes')
        PRICING = 'PRICING', _('Pricing')
        ACES = 'ACES', _('ACES Application')
        PIES = 'PIES', _('PIES Data')
    
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    
    # Source (FileMaker)
    filemaker_table = models.CharField(max_length=200)
    filemaker_field = models.CharField(max_length=200)
    
    # Target (Django)
    target_model = models.CharField(
        max_length=20,
        choices=TargetModel.choices,
        db_index=True
    )
    target_field = models.CharField(max_length=200)
    
    # Transformation
    transformation_function = models.TextField(
        blank=True,
        help_text=_('Python function name or code for data transformation')
    )
    default_value = models.CharField(max_length=500, blank=True)
    
    # Validation
    is_required = models.BooleanField(default=False)
    validation_regex = models.CharField(max_length=500, blank=True)
    
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('data mapping')
        verbose_name_plural = _('data mappings')
        unique_together = ['filemaker_table', 'filemaker_field', 'target_model', 'target_field']
        ordering = ['filemaker_table', 'filemaker_field']
        indexes = [
            models.Index(fields=['target_model', 'is_active']),
        ]
    
    def __str__(self):
        """String representation of the data mapping."""
        return f"{self.filemaker_table}.{self.filemaker_field} → {self.target_model}.{self.target_field}"


class SyncConfiguration(models.Model):
    """
    Configuration for sync schedules and settings.
    """
    
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    
    # Schedule
    is_enabled = models.BooleanField(default=True, db_index=True)
    sync_interval_minutes = models.IntegerField(
        default=60,
        help_text=_('Sync interval in minutes')
    )
    
    # FileMaker connection
    filemaker_layout = models.CharField(max_length=200)
    filemaker_query = models.TextField(
        blank=True,
        help_text=_('FileMaker find/query criteria')
    )
    
    # Sync settings
    batch_size = models.IntegerField(default=100)
    enable_incremental = models.BooleanField(default=True)
    
    # Retry settings
    max_retries = models.IntegerField(default=3)
    retry_delay_minutes = models.IntegerField(default=5)
    
    # Notifications
    notify_on_success = models.BooleanField(default=False)
    notify_on_failure = models.BooleanField(default=True)
    notification_emails = models.TextField(
        blank=True,
        help_text=_('Comma-separated email addresses')
    )
    
    last_successful_sync = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('sync configuration')
        verbose_name_plural = _('sync configurations')
        ordering = ['name']
    
    def __str__(self):
        """String representation of the sync configuration."""
        return self.name
