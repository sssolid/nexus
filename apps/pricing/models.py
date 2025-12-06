"""
Pricing models for customer-specific pricing tiers.

Supports:
- Multiple pricing tiers
- Customer-specific pricing
- Volume discounts
- Promotional pricing
"""
from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.products.models import Product


class PricingTier(models.Model):
    """
    Pricing tier definition for customer groups.
    """
    
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=50, unique=True, db_index=True)
    description = models.TextField(blank=True)
    
    # Tier configuration
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    # Priority for tier selection (higher = higher priority)
    priority = models.IntegerField(default=0, db_index=True)
    
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('pricing tier')
        verbose_name_plural = _('pricing tiers')
        ordering = ['-priority', 'name']
    
    def __str__(self):
        """String representation of the pricing tier."""
        return f"{self.name} ({self.discount_percentage}% discount)"


class CustomerProductPrice(models.Model):
    """
    Customer-specific pricing for individual products.
    Overrides tier pricing for specific customers.
    """
    
    customer = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'CUSTOMER'},
        related_name='custom_prices'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='customer_prices'
    )
    
    # Custom price
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Validity period
    effective_date = models.DateField(default=timezone.now)
    expiration_date = models.DateField(blank=True, null=True)
    
    is_active = models.BooleanField(default=True, db_index=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_prices'
    )
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('customer product price')
        verbose_name_plural = _('customer product prices')
        unique_together = ['customer', 'product', 'effective_date']
        ordering = ['-effective_date']
        indexes = [
            models.Index(fields=['customer', 'product', 'is_active']),
            models.Index(fields=['effective_date', 'expiration_date']),
        ]
    
    def __str__(self):
        """String representation of the customer product price."""
        return f"{self.customer.email} - {self.product.part_number}: ${self.price}"
    
    def is_valid(self):
        """Check if price is currently valid."""
        today = timezone.now().date()
        if not self.is_active:
            return False
        if self.effective_date > today:
            return False
        if self.expiration_date and self.expiration_date < today:
            return False
        return True


class TierProductPrice(models.Model):
    """
    Tier-specific pricing for products.
    Overrides base pricing for specific tiers.
    """
    
    tier = models.ForeignKey(
        PricingTier,
        on_delete=models.CASCADE,
        related_name='product_prices'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='tier_prices'
    )
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Validity period
    effective_date = models.DateField(default=timezone.now)
    expiration_date = models.DateField(blank=True, null=True)
    
    is_active = models.BooleanField(default=True, db_index=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('tier product price')
        verbose_name_plural = _('tier product prices')
        unique_together = ['tier', 'product', 'effective_date']
        ordering = ['-effective_date']
        indexes = [
            models.Index(fields=['tier', 'is_active']),
            models.Index(fields=['product', 'is_active']),
        ]
    
    def __str__(self):
        """String representation of the tier product price."""
        return f"{self.tier.name} - {self.product.part_number}: ${self.price}"


class VolumeDiscount(models.Model):
    """
    Volume-based discounts for quantity purchases.
    """
    
    tier = models.ForeignKey(
        PricingTier,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='volume_discounts',
        help_text=_('Leave blank for universal discount')
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='volume_discounts',
        help_text=_('Leave blank for category-wide discount')
    )
    
    # Quantity thresholds
    minimum_quantity = models.IntegerField(validators=[MinValueValidator(1)])
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('volume discount')
        verbose_name_plural = _('volume discounts')
        ordering = ['minimum_quantity']
        indexes = [
            models.Index(fields=['product', 'is_active']),
            models.Index(fields=['tier', 'is_active']),
        ]
    
    def __str__(self):
        """String representation of the volume discount."""
        target = self.product.part_number if self.product else "All Products"
        tier_str = f" - {self.tier.name}" if self.tier else ""
        return f"{target}{tier_str}: {self.discount_percentage}% off {self.minimum_quantity}+ units"
