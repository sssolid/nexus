"""Admin configuration for the data_sync application."""
from django.contrib import admin
from .models import SyncJob, SyncLog, DataMapping, SyncConfiguration

@admin.register(SyncJob)
class SyncJobAdmin(admin.ModelAdmin):
    list_display = ['sync_type', 'status', 'filemaker_layout', 'records_fetched', 'created_at']
    list_filter = ['sync_type', 'status']
    search_fields = ['filemaker_layout']

@admin.register(SyncLog)
class SyncLogAdmin(admin.ModelAdmin):
    list_display = ['sync_job', 'level', 'message', 'created_at']
    list_filter = ['level']

@admin.register(DataMapping)
class DataMappingAdmin(admin.ModelAdmin):
    list_display = ['name', 'filemaker_table', 'target_model', 'is_active']
    list_filter = ['target_model', 'is_active']
    search_fields = ['name', 'filemaker_table']

@admin.register(SyncConfiguration)
class SyncConfigurationAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_enabled', 'sync_interval_minutes', 'last_successful_sync']
    list_filter = ['is_enabled']
    search_fields = ['name']
