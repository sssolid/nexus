"""
Celery tasks for data synchronization.
"""

from celery import shared_task
from django.utils import timezone


@shared_task
def sync_filemaker_data():
    """
    Synchronize data from FileMaker.
    Runs hourly via Celery Beat.
    """
    from apps.products.models import Product

    from .models import SyncConfiguration, SyncJob, SyncLog

    # Get active sync configurations
    configs = SyncConfiguration.objects.filter(is_enabled=True)

    results = []
    for config in configs:
        job = SyncJob.objects.create(
            sync_type="INCREMENTAL",
            filemaker_layout=config.filemaker_layout,
            status="RUNNING",
        )
        job.started_at = timezone.now()
        job.save()

        try:
            # Mock sync logic (replace with actual FileMaker API calls)
            # This would normally fetch data from FileMaker and update Django models

            # Log sync progress
            SyncLog.objects.create(
                sync_job=job,
                level="INFO",
                message=f"Starting sync for layout: {config.filemaker_layout}",
            )

            # Simulate fetching records
            job.records_fetched = 100
            job.records_created = 5
            job.records_updated = 90
            job.records_failed = 5

            # Mark as completed
            job.status = "COMPLETED"
            job.completed_at = timezone.now()
            job.save()

            # Update config
            config.last_successful_sync = timezone.now()
            config.save()

            SyncLog.objects.create(
                sync_job=job,
                level="INFO",
                message=f"Sync completed successfully: {job.records_updated} updated, {job.records_created} created",
            )

            results.append(f"Synced {config.name}: {job.records_fetched} records")

        except Exception as e:
            job.status = "FAILED"
            job.error_message = str(e)
            job.completed_at = timezone.now()
            job.save()

            SyncLog.objects.create(
                sync_job=job, level="ERROR", message=f"Sync failed: {str(e)}"
            )

            results.append(f"Failed to sync {config.name}: {str(e)}")

    return results


@shared_task
def validate_product_data():
    """
    Run validation checks on product data.
    """
    from apps.products.models import Product
    from apps.validator.models import ValidationError, ValidationJob

    issues = []

    # Check for products without images
    products_without_images = Product.objects.filter(
        is_active=True, images__isnull=True
    ).count()

    if products_without_images > 0:
        issues.append(f"{products_without_images} products missing images")

    # Check for products with zero price
    zero_price_products = Product.objects.filter(is_active=True, base_price=0).count()

    if zero_price_products > 0:
        issues.append(f"{zero_price_products} products with zero price")

    # Check for products with no stock and not discontinued
    no_stock_products = (
        Product.objects.filter(is_active=True, quantity_in_stock=0)
        .exclude(status="DISCONTINUED")
        .count()
    )

    if no_stock_products > 0:
        issues.append(f"{no_stock_products} products out of stock")

    return issues if issues else ["No data quality issues found"]


@shared_task
def cleanup_old_sync_logs():
    """
    Delete sync logs older than 90 days.
    """
    from datetime import timedelta

    from .models import SyncLog

    cutoff_date = timezone.now() - timedelta(days=90)

    old_logs = SyncLog.objects.filter(created_at__lt=cutoff_date)
    count = old_logs.count()
    old_logs.delete()

    return f"Deleted {count} old sync logs"
