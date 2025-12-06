"""
Product models for the Automotive Catalog System.

Implements the core product catalog with support for:
- Product hierarchy (categories, subcategories)
- Custom attributes (avoiding JSON fields for performance)
- Product variations and packages
- Full-text search optimization
"""
from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class ProductCategory(models.Model):
    """
    Product category for organizing products hierarchically.
    """
    
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    
    display_order = models.IntegerField(default=0, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('product category')
        verbose_name_plural = _('product categories')
        ordering = ['display_order', 'name']
        indexes = [
            models.Index(fields=['parent', 'is_active']),
        ]
    
    def __str__(self):
        """String representation of the category."""
        return self.name
    
    def save(self, *args, **kwargs):
        """Auto-generate slug from name."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProductManufacturer(models.Model):
    """
    Product manufacturer/brand information.
    """
    
    name = models.CharField(max_length=200, unique=True, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    code = models.CharField(max_length=50, unique=True, db_index=True)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='manufacturers/', blank=True, null=True)
    
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('manufacturer')
        verbose_name_plural = _('manufacturers')
        ordering = ['name']
    
    def __str__(self):
        """String representation of the manufacturer."""
        return self.name


class Product(models.Model):
    """
    Core product model with optimized structure for large catalogs.
    """
    
    class ProductStatus(models.TextChoices):
        """Product status choices."""
        ACTIVE = 'ACTIVE', _('Active')
        DISCONTINUED = 'DISCONTINUED', _('Discontinued')
        PENDING = 'PENDING', _('Pending')
        OUT_OF_STOCK = 'OUT_OF_STOCK', _('Out of Stock')
    
    # Primary identification
    part_number = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text=_('Internal part number')
    )
    manufacturer_part_number = models.CharField(
        max_length=100,
        db_index=True,
        help_text=_('Manufacturer part number')
    )
    upc = models.CharField(
        max_length=20,
        blank=True,
        db_index=True,
        help_text=_('Universal Product Code')
    )
    ean = models.CharField(
        max_length=20,
        blank=True,
        help_text=_('European Article Number')
    )
    
    # Basic information
    name = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500, unique=True, db_index=True)
    description = models.TextField(blank=True)
    long_description = models.TextField(blank=True)
    
    # Classification
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.PROTECT,
        related_name='products'
    )
    manufacturer = models.ForeignKey(
        ProductManufacturer,
        on_delete=models.PROTECT,
        related_name='products'
    )
    
    # Status and availability
    status = models.CharField(
        max_length=20,
        choices=ProductStatus.choices,
        default=ProductStatus.ACTIVE,
        db_index=True
    )
    is_active = models.BooleanField(default=True, db_index=True)
    is_featured = models.BooleanField(default=False, db_index=True)
    
    # Base pricing (customer-specific pricing in pricing app)
    base_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text=_('Base retail price')
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    
    # Inventory
    quantity_in_stock = models.IntegerField(default=0)
    minimum_order_quantity = models.IntegerField(default=1)
    
    # Physical attributes (commonly searched fields as dedicated columns)
    weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_('Weight in pounds')
    )
    length = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    width = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    height = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Search optimization
    search_vector = SearchVectorField(null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_synced_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['part_number']),
            models.Index(fields=['manufacturer_part_number']),
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['manufacturer', 'is_active']),
            models.Index(fields=['status', 'is_active']),
            models.Index(fields=['is_featured', 'is_active']),
            GinIndex(fields=['search_vector']),
        ]
    
    def __str__(self):
        """String representation of the product."""
        return f"{self.part_number} - {self.name}"
    
    def save(self, *args, **kwargs):
        """Auto-generate slug from part number and name."""
        if not self.slug:
            self.slug = slugify(f"{self.part_number}-{self.name}"[:500])
        super().save(*args, **kwargs)


class ProductAttribute(models.Model):
    """
    Custom product attributes with dedicated columns for performance.
    Each common attribute gets its own field to avoid JSON field performance issues.
    """
    
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name='attributes'
    )
    
    # Common automotive attributes as dedicated fields
    color = models.CharField(max_length=50, blank=True, db_index=True)
    material = models.CharField(max_length=100, blank=True, db_index=True)
    finish = models.CharField(max_length=100, blank=True)
    
    # Performance attributes
    torque_rating = models.CharField(max_length=50, blank=True)
    horsepower_rating = models.CharField(max_length=50, blank=True)
    voltage = models.CharField(max_length=20, blank=True)
    amperage = models.CharField(max_length=20, blank=True)
    
    # Dimensional attributes
    thread_size = models.CharField(max_length=50, blank=True)
    diameter = models.CharField(max_length=50, blank=True)
    bore_size = models.CharField(max_length=50, blank=True)
    
    # Compatibility
    fitment_type = models.CharField(max_length=100, blank=True, db_index=True)
    placement = models.CharField(max_length=100, blank=True)
    
    # Quality/Certification
    warranty_period = models.CharField(max_length=100, blank=True)
    certifications = models.TextField(blank=True)
    country_of_origin = models.CharField(max_length=100, blank=True)
    
    # Package contents
    pieces_per_package = models.IntegerField(blank=True, null=True)
    package_type = models.CharField(max_length=100, blank=True)
    
    # Additional searchable fields
    custom_field_1 = models.CharField(max_length=255, blank=True, db_index=True)
    custom_field_2 = models.CharField(max_length=255, blank=True, db_index=True)
    custom_field_3 = models.CharField(max_length=255, blank=True, db_index=True)
    custom_field_4 = models.TextField(blank=True)
    custom_field_5 = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('product attribute')
        verbose_name_plural = _('product attributes')
        indexes = [
            models.Index(fields=['color']),
            models.Index(fields=['material']),
            models.Index(fields=['fitment_type']),
        ]
    
    def __str__(self):
        """String representation of the product attributes."""
        return f"Attributes for {self.product.part_number}"


class ProductImage(models.Model):
    """
    Product images with support for multiple images per product.
    Optimized for the extensive media archive.
    """
    
    class ImageType(models.TextChoices):
        """Image type choices."""
        PRIMARY = 'PRIMARY', _('Primary')
        ALTERNATE = 'ALTERNATE', _('Alternate View')
        DETAIL = 'DETAIL', _('Detail')
        LIFESTYLE = 'LIFESTYLE', _('Lifestyle')
        DIAGRAM = 'DIAGRAM', _('Diagram')
        INSTALLATION = 'INSTALLATION', _('Installation')
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='products/%Y/%m/')
    image_type = models.CharField(
        max_length=20,
        choices=ImageType.choices,
        default=ImageType.ALTERNATE,
        db_index=True
    )
    alt_text = models.CharField(max_length=255, blank=True)
    caption = models.CharField(max_length=500, blank=True)
    display_order = models.IntegerField(default=0, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    
    # File metadata
    file_size = models.IntegerField(blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('product image')
        verbose_name_plural = _('product images')
        ordering = ['display_order', 'created_at']
        indexes = [
            models.Index(fields=['product', 'image_type', 'is_active']),
            models.Index(fields=['display_order']),
        ]
    
    def __str__(self):
        """String representation of the product image."""
        return f"{self.product.part_number} - {self.image_type}"


class ProductDocument(models.Model):
    """
    Product-related documents (manuals, specifications, etc.).
    """
    
    class DocumentType(models.TextChoices):
        """Document type choices."""
        MANUAL = 'MANUAL', _('Installation Manual')
        SPEC_SHEET = 'SPEC_SHEET', _('Specification Sheet')
        WARRANTY = 'WARRANTY', _('Warranty Information')
        DIAGRAM = 'DIAGRAM', _('Technical Diagram')
        CERTIFICATE = 'CERTIFICATE', _('Certificate')
        OTHER = 'OTHER', _('Other')
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    title = models.CharField(max_length=255)
    document_type = models.CharField(
        max_length=20,
        choices=DocumentType.choices,
        db_index=True
    )
    file = models.FileField(upload_to='product_documents/%Y/%m/')
    description = models.TextField(blank=True)
    version = models.CharField(max_length=50, blank=True)
    
    is_public = models.BooleanField(default=True, db_index=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('product document')
        verbose_name_plural = _('product documents')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['product', 'document_type']),
        ]
    
    def __str__(self):
        """String representation of the product document."""
        return f"{self.product.part_number} - {self.title}"


class ProductRelationship(models.Model):
    """
    Relationships between products (accessories, replacements, bundles).
    """
    
    class RelationType(models.TextChoices):
        """Relationship type choices."""
        ACCESSORY = 'ACCESSORY', _('Accessory')
        REPLACEMENT = 'REPLACEMENT', _('Replacement')
        UPGRADE = 'UPGRADE', _('Upgrade')
        RELATED = 'RELATED', _('Related Product')
        BUNDLE = 'BUNDLE', _('Bundle')
        ALTERNATIVE = 'ALTERNATIVE', _('Alternative')
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='related_products'
    )
    related_product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='related_to'
    )
    relationship_type = models.CharField(
        max_length=20,
        choices=RelationType.choices,
        db_index=True
    )
    display_order = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('product relationship')
        verbose_name_plural = _('product relationships')
        unique_together = ['product', 'related_product', 'relationship_type']
        ordering = ['display_order', 'created_at']
        indexes = [
            models.Index(fields=['product', 'relationship_type']),
        ]
    
    def __str__(self):
        """String representation of the product relationship."""
        return f"{self.product.part_number} -> {self.related_product.part_number} ({self.relationship_type})"
