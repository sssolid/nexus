"""Admin configuration for the pricing application."""
from django.contrib import admin
from .models import PricingTier, CustomerProductPrice, TierProductPrice, VolumeDiscount

@admin.register(PricingTier)
class PricingTierAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'discount_percentage', 'priority', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'code']

@admin.register(CustomerProductPrice)
class CustomerProductPriceAdmin(admin.ModelAdmin):
    list_display = ['customer', 'product', 'price', 'effective_date', 'is_active']
    list_filter = ['is_active', 'effective_date']
    search_fields = ['customer__email', 'product__part_number']

@admin.register(TierProductPrice)
class TierProductPriceAdmin(admin.ModelAdmin):
    list_display = ['tier', 'product', 'price', 'effective_date', 'is_active']
    list_filter = ['tier', 'is_active']
    search_fields = ['product__part_number']

@admin.register(VolumeDiscount)
class VolumeDiscountAdmin(admin.ModelAdmin):
    list_display = ['product', 'tier', 'minimum_quantity', 'discount_percentage', 'is_active']
    list_filter = ['is_active']
