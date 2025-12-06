"""
Admin configuration for the products application.
"""
from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Product,
    ProductAttribute,
    ProductCategory,
    ProductDocument,
    ProductImage,
    ProductManufacturer,
    ProductRelationship,
)


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    """Admin interface for ProductCategory model."""
    
    list_display = ['name', 'parent', 'display_order', 'is_active', 'created_at']
    list_filter = ['is_active', 'parent']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['display_order', 'name']


@admin.register(ProductManufacturer)
class ProductManufacturerAdmin(admin.ModelAdmin):
    """Admin interface for ProductManufacturer model."""
    
    list_display = ['name', 'code', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'code']
    prepopulated_fields = {'slug': ('name',)}


class ProductImageInline(admin.TabularInline):
    """Inline admin for product images."""
    model = ProductImage
    extra = 1
    fields = ['image', 'image_type', 'alt_text', 'display_order', 'is_active']


class ProductDocumentInline(admin.TabularInline):
    """Inline admin for product documents."""
    model = ProductDocument
    extra = 0
    fields = ['title', 'document_type', 'file', 'is_public']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin interface for Product model."""
    
    list_display = [
        'part_number', 'name', 'manufacturer', 'category',
        'base_price', 'quantity_in_stock', 'status', 'is_active'
    ]
    list_filter = ['status', 'is_active', 'is_featured', 'category', 'manufacturer']
    search_fields = ['part_number', 'manufacturer_part_number', 'name', 'upc', 'ean']
    prepopulated_fields = {'slug': ('part_number', 'name')}
    readonly_fields = ['created_at', 'updated_at', 'last_synced_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'part_number', 'manufacturer_part_number',
                'upc', 'ean', 'name', 'slug'
            )
        }),
        ('Classification', {
            'fields': ('category', 'manufacturer')
        }),
        ('Description', {
            'fields': ('description', 'long_description')
        }),
        ('Pricing & Inventory', {
            'fields': ('base_price', 'cost', 'quantity_in_stock', 'minimum_order_quantity')
        }),
        ('Physical Attributes', {
            'fields': ('weight', 'length', 'width', 'height'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('status', 'is_active', 'is_featured')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'last_synced_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [ProductImageInline, ProductDocumentInline]


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    """Admin interface for ProductAttribute model."""
    
    list_display = ['product', 'color', 'material', 'fitment_type']
    search_fields = ['product__part_number', 'color', 'material']
    list_filter = ['color', 'material', 'fitment_type']


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """Admin interface for ProductImage model."""
    
    list_display = ['product', 'image_type', 'display_order', 'is_active']
    list_filter = ['image_type', 'is_active']
    search_fields = ['product__part_number', 'alt_text']


@admin.register(ProductDocument)
class ProductDocumentAdmin(admin.ModelAdmin):
    """Admin interface for ProductDocument model."""
    
    list_display = ['product', 'title', 'document_type', 'is_public']
    list_filter = ['document_type', 'is_public']
    search_fields = ['product__part_number', 'title']


@admin.register(ProductRelationship)
class ProductRelationshipAdmin(admin.ModelAdmin):
    """Admin interface for ProductRelationship model."""
    
    list_display = ['product', 'related_product', 'relationship_type', 'display_order']
    list_filter = ['relationship_type']
    search_fields = ['product__part_number', 'related_product__part_number']
