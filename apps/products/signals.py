"""
Signals for the products application.

Handles automatic updates like search vector updates.
"""
from django.contrib.postgres.search import SearchVector
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Product


@receiver(post_save, sender=Product)
def update_product_search_vector(sender, instance, **kwargs):
    """
    Update search vector when product is saved.
    
    Args:
        sender: The Product model class
        instance: The Product instance being saved
        **kwargs: Additional keyword arguments
    """
    # Update search vector for full-text search
    Product.objects.filter(pk=instance.pk).update(
        search_vector=SearchVector('part_number', 'name', 'description', 'manufacturer_part_number')
    )
