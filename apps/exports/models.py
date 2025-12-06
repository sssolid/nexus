"""
Exports models for product data delivery.

Supports:
- Multiple export formats (CSV, Excel, JSON, XML)
- Scheduled exports
- Multiple delivery methods (Email, SFTP, Direct Download)
- Export templates and configurations
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class ExportTemplate(models.Model):
    """
    Export template defining which fields and format to export.
    """
    
    class ExportFormat(models.TextChoices):
        """Export format choices."""
        CSV = 'CSV', _('CSV')
        EXCEL = 'EXCEL', _('Excel (XLSX)')
        JSON = 'JSON', _('JSON')
        XML = 'XML', _('XML')
        PDF = 'PDF', _('PDF')
    
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    format = models.CharField(
        max_length=10,
        choices=ExportFormat.choices,
        default=ExportFormat.CSV,
        db_index=True
    )
    
    # Field configuration (stored as comma-separated field names)
    included_fields = models.TextField(
        help_text=_('Comma-separated list of field names to include')
    )
    
    # Filters
    filter_config = models.JSONField(
        blank=True,
        null=True,
        help_text=_('JSON configuration for filtering products')
    )
    
    # Template accessibility
    is_public = models.BooleanField(
        default=False,
        help_text=_('Available to all users')
    )
    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_templates'
    )
    
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('export template')
        verbose_name_plural = _('export templates')
        ordering = ['name']
    
    def __str__(self):
        """String representation of the export template."""
        return f"{self.name} ({self.format})"


class ExportJob(models.Model):
    """
    Export job tracking individual export requests.
    """
    
    class JobStatus(models.TextChoices):
        """Job status choices."""
        PENDING = 'PENDING', _('Pending')
        PROCESSING = 'PROCESSING', _('Processing')
        COMPLETED = 'COMPLETED', _('Completed')
        FAILED = 'FAILED', _('Failed')
        CANCELLED = 'CANCELLED', _('Cancelled')
    
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='export_jobs'
    )
    template = models.ForeignKey(
        ExportTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='export_jobs'
    )
    
    # Job details
    name = models.CharField(max_length=200)
    status = models.CharField(
        max_length=20,
        choices=JobStatus.choices,
        default=JobStatus.PENDING,
        db_index=True
    )
    
    # Export configuration
    format = models.CharField(max_length=10, db_index=True)
    total_records = models.IntegerField(default=0)
    processed_records = models.IntegerField(default=0)
    
    # Output file
    file = models.FileField(upload_to='exports/%Y/%m/%d/', blank=True, null=True)
    file_size = models.BigIntegerField(blank=True, null=True)
    
    # Error tracking
    error_message = models.TextField(blank=True)
    
    # Timing
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('export job')
        verbose_name_plural = _('export jobs')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['status', 'created_at']),
        ]
    
    def __str__(self):
        """String representation of the export job."""
        return f"{self.name} - {self.status}"


class ScheduledExport(models.Model):
    """
    Scheduled recurring export jobs.
    """
    
    class Frequency(models.TextChoices):
        """Export frequency choices."""
        DAILY = 'DAILY', _('Daily')
        WEEKLY = 'WEEKLY', _('Weekly')
        MONTHLY = 'MONTHLY', _('Monthly')
        CUSTOM = 'CUSTOM', _('Custom Cron')
    
    class DeliveryMethod(models.TextChoices):
        """Delivery method choices."""
        EMAIL = 'EMAIL', _('Email')
        SFTP = 'SFTP', _('SFTP')
        DOWNLOAD = 'DOWNLOAD', _('Download Link')
        API = 'API', _('API Callback')
    
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='scheduled_exports'
    )
    template = models.ForeignKey(
        ExportTemplate,
        on_delete=models.CASCADE,
        related_name='scheduled_exports'
    )
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Schedule configuration
    frequency = models.CharField(
        max_length=20,
        choices=Frequency.choices,
        db_index=True
    )
    cron_expression = models.CharField(
        max_length=100,
        blank=True,
        help_text=_('For custom frequency')
    )
    
    # Delivery configuration
    delivery_method = models.CharField(
        max_length=20,
        choices=DeliveryMethod.choices,
        db_index=True
    )
    delivery_email = models.EmailField(blank=True)
    delivery_sftp_path = models.CharField(max_length=500, blank=True)
    delivery_api_url = models.URLField(blank=True)
    
    # Status
    is_active = models.BooleanField(default=True, db_index=True)
    last_run_at = models.DateTimeField(blank=True, null=True)
    next_run_at = models.DateTimeField(blank=True, null=True, db_index=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('scheduled export')
        verbose_name_plural = _('scheduled exports')
        ordering = ['next_run_at']
        indexes = [
            models.Index(fields=['is_active', 'next_run_at']),
            models.Index(fields=['user', 'is_active']),
        ]
    
    def __str__(self):
        """String representation of the scheduled export."""
        return f"{self.name} ({self.frequency})"


class ExportDeliveryLog(models.Model):
    """
    Log of export delivery attempts.
    """
    
    class DeliveryStatus(models.TextChoices):
        """Delivery status choices."""
        SUCCESS = 'SUCCESS', _('Success')
        FAILED = 'FAILED', _('Failed')
        PENDING = 'PENDING', _('Pending')
    
    scheduled_export = models.ForeignKey(
        ScheduledExport,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='delivery_logs'
    )
    export_job = models.ForeignKey(
        ExportJob,
        on_delete=models.CASCADE,
        related_name='delivery_logs'
    )
    
    delivery_method = models.CharField(max_length=20)
    status = models.CharField(
        max_length=20,
        choices=DeliveryStatus.choices,
        default=DeliveryStatus.PENDING,
        db_index=True
    )
    
    # Delivery details
    recipient = models.CharField(max_length=500, blank=True)
    error_message = models.TextField(blank=True)
    
    attempted_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name = _('export delivery log')
        verbose_name_plural = _('export delivery logs')
        ordering = ['-attempted_at']
        indexes = [
            models.Index(fields=['status', 'attempted_at']),
        ]
    
    def __str__(self):
        """String representation of the delivery log."""
        return f"{self.export_job.name} - {self.delivery_method} - {self.status}"
