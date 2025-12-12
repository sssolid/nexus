"""
Celery tasks for data synchronization.
"""
from django.apps import apps
from celery import shared_task
from django.utils import timezone

from apps.data_sync.models import SyncConfiguration, SyncJob, SyncLog
from services.filemaker_client import FileMakerClient
from services.mapping_engine import apply_mapping
from django.conf import settings


@shared_task(bind=True, max_retries=3)
def sync_filemaker_data(self):
    configs = SyncConfiguration.objects.filter(is_enabled=True)
    results = []

    client = FileMakerClient(password=settings.FILEMAKER_PASSWORD)

    for cfg in configs:
        job = SyncJob.objects.create(
            sync_type="INCREMENTAL" if cfg.enable_incremental else "FULL",
            filemaker_layout=cfg.filemaker_layout,
            status="RUNNING",
            started_at=timezone.now(),
        )

        try:
            # Query FileMaker
            fm_query = cfg.filemaker_query or None
            fm_rows = client.fetch(cfg.filemaker_layout, fm_query)

            job.records_fetched = len(fm_rows)
            job.save()

            # Determine target Django model
            TargetModel = apps.get_model("products", cfg.target_model_name)

            to_create = []
            to_update = []
            existing = {
                obj.external_id: obj
                for obj in TargetModel.objects.filter(
                    external_id__in=[r["id"] for r in fm_rows]
                )
            }

            for row in fm_rows:
                mapped = apply_mapping(row, cfg.target_model)

                external_id = mapped["external_id"]

                if external_id in existing:
                    obj = existing[external_id]
                    for k, v in mapped.items():
                        setattr(obj, k, v)
                    to_update.append(obj)
                else:
                    to_create.append(TargetModel(**mapped))

            # Bulk operations
            if to_create:
                TargetModel.objects.bulk_create(to_create, batch_size=cfg.batch_size)

            if to_update:
                TargetModel.objects.bulk_update(
                    to_update,
                    fields=list(mapped.keys()),
                    batch_size=cfg.batch_size,
                )

            # Finalize job
            job.records_created = len(to_create)
            job.records_updated = len(to_update)
            job.status = "COMPLETED"
            job.completed_at = timezone.now()
            job.save()

            cfg.last_successful_sync = timezone.now()
            cfg.save()

            results.append(f"Synced {cfg.name}: {job.records_fetched}")

        except Exception as e:
            job.status = "FAILED"
            job.error_message = str(e)
            job.completed_at = timezone.now()
            job.save()

            SyncLog.objects.create(
                sync_job=job,
                level="ERROR",
                message=f"Sync failed: {str(e)}",
            )

            results.append(f"Failed {cfg.name}: {str(e)}")

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
