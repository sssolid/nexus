"""
Celery tasks for products application.
"""

from celery import shared_task
from django.contrib.postgres.search import SearchVector
from django.core.cache import cache
from django.db.models import Prefetch

from .models import Product, ProductCategory, ProductManufacturer


@shared_task
def update_search_index():
    """
    Update search vectors for all products.
    Scheduled to run nightly.
    """
    products = Product.objects.all()

    for product in products.iterator(chunk_size=100):
        product.search_vector = SearchVector(
            "part_number", "name", "description", "manufacturer_part_number"
        )
        product.save(update_fields=["search_vector"])

    return f"Updated search index for {products.count()} products"


@shared_task
def warm_product_cache():
    """
    Warm frequently accessed product data in cache.
    """
    # Cache featured products
    featured_products = list(
        Product.objects.filter(is_featured=True, is_active=True)
        .select_related("category", "manufacturer")
        .prefetch_related("images")[:10]
    )
    cache.set("featured_products", featured_products, timeout=3600)

    # Cache active categories
    categories = list(
        ProductCategory.objects.filter(is_active=True).prefetch_related("children")
    )
    cache.set("active_categories", categories, timeout=7200)

    # Cache manufacturers
    manufacturers = list(ProductManufacturer.objects.filter(is_active=True))
    cache.set("active_manufacturers", manufacturers, timeout=7200)

    return "Cache warmed successfully"


@shared_task
def cleanup_old_images():
    """
    Clean up unused product images.
    """
    from datetime import timedelta

    from django.utils import timezone

    # Find images older than 90 days that aren't active
    cutoff_date = timezone.now() - timedelta(days=90)

    from .models import ProductImage

    old_images = ProductImage.objects.filter(
        is_active=False, created_at__lt=cutoff_date
    )

    count = old_images.count()
    old_images.delete()

    return f"Cleaned up {count} old images"


@shared_task
def generate_product_report():
    """
    Generate product statistics report.
    """
    stats = {
        "total_products": Product.objects.filter(is_active=True).count(),
        "featured_products": Product.objects.filter(
            is_featured=True, is_active=True
        ).count(),
        "out_of_stock": Product.objects.filter(
            quantity_in_stock=0, is_active=True
        ).count(),
        "discontinued": Product.objects.filter(status="DISCONTINUED").count(),
    }

    # Cache the stats
    cache.set("product_stats", stats, timeout=3600)

    return stats
