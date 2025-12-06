"""Admin configuration for the exports application."""
from django.contrib import admin
from .models import ExportTemplate, ExportJob, ScheduledExport, ExportDeliveryLog

@admin.register(ExportTemplate)
class ExportTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'format', 'is_public', 'is_active', 'created_by']
    list_filter = ['format', 'is_public', 'is_active']
    search_fields = ['name']

@admin.register(ExportJob)
class ExportJobAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'status', 'format', 'created_at']
    list_filter = ['status', 'format']
    search_fields = ['name', 'user__email']

@admin.register(ScheduledExport)
class ScheduledExportAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'frequency', 'delivery_method', 'is_active']
    list_filter = ['frequency', 'delivery_method', 'is_active']
    search_fields = ['name', 'user__email']

@admin.register(ExportDeliveryLog)
class ExportDeliveryLogAdmin(admin.ModelAdmin):
    list_display = ['export_job', 'delivery_method', 'status', 'attempted_at']
    list_filter = ['status', 'delivery_method']
