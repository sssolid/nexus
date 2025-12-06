"""
ACES and PIES models for automotive fitment and product data.

ACES (Aftermarket Catalog Exchange Standard) - Vehicle application data
PIES (Product Information Exchange Standard) - Product content data

These models handle extensive fitment data with optimized structure for performance.
"""
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.products.models import Product


class VehicleMake(models.Model):
    """
    Vehicle make (manufacturer) reference data.
    """
    
    name = models.CharField(max_length=100, unique=True, db_index=True)
    code = models.CharField(max_length=20, unique=True, db_index=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('vehicle make')
        verbose_name_plural = _('vehicle makes')
        ordering = ['name']
    
    def __str__(self):
        """String representation of the vehicle make."""
        return self.name


class VehicleModel(models.Model):
    """
    Vehicle model reference data.
    """
    
    make = models.ForeignKey(
        VehicleMake,
        on_delete=models.CASCADE,
        related_name='models'
    )
    name = models.CharField(max_length=100, db_index=True)
    code = models.CharField(max_length=50, db_index=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('vehicle model')
        verbose_name_plural = _('vehicle models')
        ordering = ['make__name', 'name']
        unique_together = ['make', 'code']
        indexes = [
            models.Index(fields=['make', 'name']),
        ]
    
    def __str__(self):
        """String representation of the vehicle model."""
        return f"{self.make.name} {self.name}"


class VehicleApplication(models.Model):
    """
    ACES vehicle application data linking products to specific vehicles.
    Partitioned by year ranges for performance with large datasets.
    """
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='vehicle_applications',
        db_index=True
    )
    
    # Vehicle identification
    make = models.ForeignKey(
        VehicleMake,
        on_delete=models.PROTECT,
        related_name='applications'
    )
    model = models.ForeignKey(
        VehicleModel,
        on_delete=models.PROTECT,
        related_name='applications'
    )
    year = models.IntegerField(db_index=True)
    submodel = models.CharField(max_length=100, blank=True, db_index=True)
    
    # Engine specifications
    engine_base = models.CharField(max_length=50, blank=True, db_index=True)
    engine_designation = models.CharField(max_length=100, blank=True)
    engine_vin = models.CharField(max_length=20, blank=True, db_index=True)
    liter = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    cylinders = models.IntegerField(blank=True, null=True)
    block_type = models.CharField(max_length=10, blank=True)
    fuel_type = models.CharField(max_length=50, blank=True, db_index=True)
    
    # Drive and transmission
    drive_type = models.CharField(max_length=50, blank=True)
    transmission = models.CharField(max_length=100, blank=True)
    
    # Body and configuration
    body_type = models.CharField(max_length=50, blank=True, db_index=True)
    bed_length = models.CharField(max_length=50, blank=True)
    wheelbase = models.CharField(max_length=50, blank=True)
    
    # Position and quantity
    position = models.CharField(max_length=100, blank=True, help_text=_('e.g., Front, Rear, Left, Right'))
    quantity = models.IntegerField(default=1)
    
    # Notes and qualifiers
    note = models.TextField(blank=True)
    qualifier = models.CharField(max_length=500, blank=True)
    
    # Search optimization
    search_vector = SearchVectorField(null=True, blank=True)
    
    # Metadata
    aces_version = models.CharField(max_length=10, default='5.0')
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('vehicle application')
        verbose_name_plural = _('vehicle applications')
        ordering = ['-year', 'make__name', 'model__name']
        indexes = [
            models.Index(fields=['product', 'is_active']),
            models.Index(fields=['make', 'model', 'year']),
            models.Index(fields=['year', 'make']),
            models.Index(fields=['engine_base']),
            models.Index(fields=['engine_vin']),
            models.Index(fields=['fuel_type']),
            models.Index(fields=['body_type']),
            GinIndex(fields=['search_vector']),
        ]
    
    def __str__(self):
        """String representation of the vehicle application."""
        return f"{self.year} {self.make.name} {self.model.name} - {self.product.part_number}"


class PIESItem(models.Model):
    """
    PIES product information for enhanced product data.
    Extends product model with PIES-specific fields.
    """
    
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name='pies_data'
    )
    
    # PIES Identifiers
    pies_item_number = models.CharField(max_length=100, unique=True, db_index=True)
    brand_label = models.CharField(max_length=100, db_index=True)
    hazmat_code = models.CharField(max_length=50, blank=True)
    
    # Package information
    package_uom = models.CharField(max_length=50, blank=True)
    quantity_per_package = models.IntegerField(default=1)
    package_height = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    package_length = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    package_width = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    package_weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Shipping information
    shipping_height = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    shipping_length = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    shipping_width = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    shipping_weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Country information
    country_of_origin = models.CharField(max_length=100, blank=True)
    
    # Product status
    replacement_part_number = models.CharField(max_length=100, blank=True, db_index=True)
    vmrs_code = models.CharField(max_length=50, blank=True)
    unspsc_code = models.CharField(max_length=50, blank=True)
    
    # Metadata
    pies_version = models.CharField(max_length=10, default='7.2')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('PIES item')
        verbose_name_plural = _('PIES items')
        indexes = [
            models.Index(fields=['pies_item_number']),
            models.Index(fields=['brand_label']),
            models.Index(fields=['replacement_part_number']),
        ]
    
    def __str__(self):
        """String representation of the PIES item."""
        return f"PIES data for {self.product.part_number}"


class PIESDescription(models.Model):
    """
    PIES product descriptions in multiple types and languages.
    """
    
    class DescriptionType(models.TextChoices):
        """Description type choices."""
        SHORT = 'SHO', _('Short Description')
        LONG = 'LON', _('Long Description')
        EXTENDED = 'EXT', _('Extended Description')
        MARKETING = 'MKT', _('Marketing Description')
        FEATURES = 'FEA', _('Features')
        WARRANTY = 'WAR', _('Warranty')
    
    pies_item = models.ForeignKey(
        PIESItem,
        on_delete=models.CASCADE,
        related_name='descriptions'
    )
    description_type = models.CharField(
        max_length=3,
        choices=DescriptionType.choices,
        db_index=True
    )
    description_text = models.TextField()
    language_code = models.CharField(max_length=10, default='EN', db_index=True)
    sequence = models.IntegerField(default=1)
    
    class Meta:
        verbose_name = _('PIES description')
        verbose_name_plural = _('PIES descriptions')
        ordering = ['sequence']
        unique_together = ['pies_item', 'description_type', 'language_code', 'sequence']
    
    def __str__(self):
        """String representation of the PIES description."""
        return f"{self.pies_item.product.part_number} - {self.description_type}"
