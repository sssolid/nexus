"""
Caching utilities for Crown Nexus.

Provides helper functions for caching common data patterns.
"""

import hashlib
import json
from functools import wraps

from django.core.cache import cache
from django.db.models import Prefetch


def cache_key(*args, **kwargs):
    """
    Generate a cache key from arguments.
    """
    key_data = f"{args}:{sorted(kwargs.items())}"
    return hashlib.md5(key_data.encode()).hexdigest()


def cached_query(timeout=300, key_prefix="query"):
    """
    Decorator to cache database query results.

    Usage:
        @cached_query(timeout=600, key_prefix='products')
        def get_featured_products():
            return Product.objects.filter(is_featured=True)
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key_str = f"{key_prefix}:{cache_key(*args, **kwargs)}"

            # Try to get from cache
            result = cache.get(cache_key_str)

            if result is None:
                # Execute query and cache result
                result = func(*args, **kwargs)
                cache.set(cache_key_str, result, timeout=timeout)

            return result

        return wrapper

    return decorator


class ProductCache:
    """Product-specific caching utilities."""

    @staticmethod
    def get_featured_products(limit=10):
        """Get featured products from cache or database."""
        cache_key = f"featured_products:{limit}"
        products = cache.get(cache_key)

        if products is None:
            from apps.products.models import Product

            products = list(
                Product.objects.filter(is_featured=True, is_active=True)
                .select_related("category", "manufacturer")
                .prefetch_related("images")[:limit]
            )

            cache.set(cache_key, products, timeout=3600)

        return products

    @staticmethod
    def get_product_by_slug(slug):
        """Get product by slug from cache."""
        cache_key = f"product:slug:{slug}"
        product = cache.get(cache_key)

        if product is None:
            from apps.products.models import Product

            try:
                product = (
                    Product.objects.select_related("category", "manufacturer")
                    .prefetch_related("images", "documents", "attributes")
                    .get(slug=slug, is_active=True)
                )

                cache.set(cache_key, product, timeout=1800)
            except Product.DoesNotExist:
                return None

        return product

    @staticmethod
    def invalidate_product(product_id):
        """Invalidate all caches for a product."""
        from apps.products.models import Product

        try:
            product = Product.objects.get(id=product_id)
            cache.delete(f"product:slug:{product.slug}")
            cache.delete(f"product:id:{product.id}")
            cache.delete("featured_products:10")
        except Product.DoesNotExist:
            pass


class CategoryCache:
    """Category-specific caching utilities."""

    @staticmethod
    def get_category_tree():
        """Get full category tree from cache."""
        cache_key = "category_tree"
        categories = cache.get(cache_key)

        if categories is None:
            from apps.products.models import ProductCategory

            categories = list(
                ProductCategory.objects.filter(is_active=True).prefetch_related(
                    "children"
                )
            )

            cache.set(cache_key, categories, timeout=7200)

        return categories

    @staticmethod
    def get_active_categories():
        """Get all active categories from cache."""
        cache_key = "active_categories"
        categories = cache.get(cache_key)

        if categories is None:
            from apps.products.models import ProductCategory

            categories = list(ProductCategory.objects.filter(is_active=True))

            cache.set(cache_key, categories, timeout=7200)

        return categories


class UserCache:
    """User-specific caching utilities."""

    @staticmethod
    def get_user_pricing_tier(user_id):
        """Get user's active pricing tier from cache."""
        cache_key = f"user:pricing_tier:{user_id}"
        tier = cache.get(cache_key)

        if tier is None:
            from apps.accounts.models import CustomerPricingTier

            try:
                tier_assignment = (
                    CustomerPricingTier.objects.filter(user_id=user_id, is_active=True)
                    .select_related("tier")
                    .first()
                )

                tier = tier_assignment.tier if tier_assignment else None
                cache.set(cache_key, tier, timeout=3600)
            except Exception:
                tier = None

        return tier

    @staticmethod
    def invalidate_user_cache(user_id):
        """Invalidate all caches for a user."""
        cache.delete(f"user:pricing_tier:{user_id}")
        cache.delete(f"user:profile:{user_id}")


class SearchCache:
    """Search results caching utilities."""

    @staticmethod
    def get_search_results(query, filters=None, page=1):
        """Get search results from cache."""
        filter_str = json.dumps(filters or {}, sort_keys=True)
        cache_key = (
            f"search:{hashlib.md5(f'{query}:{filter_str}:{page}'.encode()).hexdigest()}"
        )

        results = cache.get(cache_key)

        if results is None:
            # Results not in cache, would perform search here
            # For now, return None to indicate cache miss
            return None

        return results

    @staticmethod
    def set_search_results(query, filters, page, results):
        """Cache search results."""
        filter_str = json.dumps(filters or {}, sort_keys=True)
        cache_key = (
            f"search:{hashlib.md5(f'{query}:{filter_str}:{page}'.encode()).hexdigest()}"
        )

        cache.set(cache_key, results, timeout=600)


def warm_cache():
    """
    Warm up commonly accessed cache entries.
    Can be called on deployment or via management command.
    """
    ProductCache.get_featured_products(10)
    CategoryCache.get_category_tree()
    CategoryCache.get_active_categories()

    return "Cache warmed successfully"
