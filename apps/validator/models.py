"""
Validator models for product data validation.

Supports:
- File upload and parsing
- Validation rules
- Error tracking and correction suggestions
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class ValidationJob(models.Model):
    """
    Validation job tracking uploaded files for validation.
    """
    
    class JobStatus(models.TextChoices):
        """Job status choices."""
        PENDING = 'PENDING', _('Pending')
        PROCESSING = 'PROCESSING', _('Processing')
        COMPLETED = 'COMPLETED', _('Completed')
        FAILED = 'FAILED', _('Failed')
    
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='validation_jobs'
    )
    
    # File information
    uploaded_file = models.FileField(upload_to='validation_uploads/%Y/%m/%d/')
    original_filename = models.CharField(max_length=255)
    file_size = models.BigIntegerField()
    
    # Job details
    status = models.CharField(
        max_length=20,
        choices=JobStatus.choices,
        default=JobStatus.PENDING,
        db_index=True
    )
    
    # Statistics
    total_rows = models.IntegerField(default=0)
    processed_rows = models.IntegerField(default=0)
    valid_rows = models.IntegerField(default=0)
    invalid_rows = models.IntegerField(default=0)
    corrected_rows = models.IntegerField(default=0)
    
    # Output files
    validated_file = models.FileField(
        upload_to='validation_results/%Y/%m/%d/',
        blank=True,
        null=True
    )
    error_report = models.FileField(
        upload_to='validation_reports/%Y/%m/%d/',
        blank=True,
        null=True
    )
    
    # Error tracking
    error_message = models.TextField(blank=True)
    
    # Timing
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('validation job')
        verbose_name_plural = _('validation jobs')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['status', 'created_at']),
        ]
    
    def __str__(self):
        """String representation of the validation job."""
        return f"{self.original_filename} - {self.status}"


class ValidationError(models.Model):
    """
    Individual validation errors found during processing.
    """
    
    class ErrorSeverity(models.TextChoices):
        """Error severity choices."""
        ERROR = 'ERROR', _('Error')
        WARNING = 'WARNING', _('Warning')
        INFO = 'INFO', _('Info')
    
    validation_job = models.ForeignKey(
        ValidationJob,
        on_delete=models.CASCADE,
        related_name='errors'
    )
    
    # Error location
    row_number = models.IntegerField(db_index=True)
    column_name = models.CharField(max_length=100, blank=True)
    
    # Error details
    severity = models.CharField(
        max_length=20,
        choices=ErrorSeverity.choices,
        default=ErrorSeverity.ERROR,
        db_index=True
    )
    error_code = models.CharField(max_length=50, db_index=True)
    error_message = models.TextField()
    
    # Original and corrected values
    original_value = models.TextField(blank=True)
    suggested_value = models.TextField(blank=True)
    was_corrected = models.BooleanField(default=False, db_index=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('validation error')
        verbose_name_plural = _('validation errors')
        ordering = ['row_number']
        indexes = [
            models.Index(fields=['validation_job', 'severity']),
            models.Index(fields=['error_code']),
        ]
    
    def __str__(self):
        """String representation of the validation error."""
        return f"Row {self.row_number}: {self.error_code}"


class ValidationRule(models.Model):
    """
    Validation rules for product data.
    """
    
    class RuleType(models.TextChoices):
        """Rule type choices."""
        REQUIRED = 'REQUIRED', _('Required Field')
        FORMAT = 'FORMAT', _('Format Validation')
        RANGE = 'RANGE', _('Range Validation')
        REFERENCE = 'REFERENCE', _('Reference Check')
        CUSTOM = 'CUSTOM', _('Custom Logic')
    
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    rule_type = models.CharField(
        max_length=20,
        choices=RuleType.choices,
        db_index=True
    )
    
    # Rule configuration
    field_name = models.CharField(max_length=100, db_index=True)
    validation_expression = models.TextField(
        help_text=_('Regex or Python expression for validation')
    )
    error_message = models.CharField(max_length=500)
    
    # Auto-correction
    can_autocorrect = models.BooleanField(default=False)
    correction_logic = models.TextField(
        blank=True,
        help_text=_('Python code for auto-correction')
    )
    
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('validation rule')
        verbose_name_plural = _('validation rules')
        ordering = ['field_name', 'name']
    
    def __str__(self):
        """String representation of the validation rule."""
        return f"{self.name} ({self.field_name})"
