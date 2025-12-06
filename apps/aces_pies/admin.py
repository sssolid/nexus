"""Admin configuration for the ACES/PIES application."""
from django.contrib import admin
from .models import VehicleMake, VehicleModel, VehicleApplication, PIESItem, PIESDescription

@admin.register(VehicleMake)
class VehicleMakeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'created_at']
    search_fields = ['name', 'code']

@admin.register(VehicleModel)
class VehicleModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'make', 'code']
    list_filter = ['make']
    search_fields = ['name', 'code']

@admin.register(VehicleApplication)
class VehicleApplicationAdmin(admin.ModelAdmin):
    list_display = ['product', 'year', 'make', 'model', 'is_active']
    list_filter = ['year', 'make', 'is_active']
    search_fields = ['product__part_number', 'make__name', 'model__name']

@admin.register(PIESItem)
class PIESItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'pies_item_number', 'brand_label']
    search_fields = ['pies_item_number', 'product__part_number']

@admin.register(PIESDescription)
class PIESDescriptionAdmin(admin.ModelAdmin):
    list_display = ['pies_item', 'description_type', 'language_code']
    list_filter = ['description_type', 'language_code']
