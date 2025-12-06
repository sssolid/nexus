"""Admin configuration for the validator application."""
from django.contrib import admin
from .models import ValidationJob, ValidationError, ValidationRule

@admin.register(ValidationJob)
class ValidationJobAdmin(admin.ModelAdmin):
    list_display = ['original_filename', 'user', 'status', 'total_rows', 'valid_rows', 'created_at']
    list_filter = ['status']
    search_fields = ['original_filename', 'user__email']

@admin.register(ValidationError)
class ValidationErrorAdmin(admin.ModelAdmin):
    list_display = ['validation_job', 'row_number', 'severity', 'error_code']
    list_filter = ['severity', 'error_code']

@admin.register(ValidationRule)
class ValidationRuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'field_name', 'rule_type', 'can_autocorrect', 'is_active']
    list_filter = ['rule_type', 'can_autocorrect', 'is_active']
    search_fields = ['name', 'field_name']
