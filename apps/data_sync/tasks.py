"""
Celery tasks for FileMaker data synchronization.
"""
from datetime import timedelta

from celery import shared_task
from django.apps import apps
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify

from apps.data_sync.models import SyncConfiguration, SyncJob, SyncLog
from services.filemaker_client import FileMakerClient
from services.mapping_engine import apply_mapping


@shared_task(bind=True, max_retries=3)
def sync_filemaker_data(self):
    now = timezone.now()

    client = FileMakerClient(password=settings.FILEMAKER_PASSWORD)

    Product = apps.get_model("products", "Product")
    ProductCategory = apps.get_model("products", "ProductCategory")
    ProductManufacturer = apps.get_model("products", "ProductManufacturer")

    default_category = ProductCategory.objects.get(slug="uncategorized")
    default_manufacturer = ProductManufacturer.objects.get(code="UNKNOWN")

    configs = SyncConfiguration.objects.filter(is_enabled=True)

    results = []

    for cfg in configs:
        # ------------------------------------------------------------
        # Enforce per-config interval
        # ------------------------------------------------------------
        if cfg.last_successful_sync:
            next_run = cfg.last_successful_sync + timedelta(
                minutes=cfg.sync_interval_minutes
            )
            if now < next_run:
                continue

        job = SyncJob.objects.create(
            sync_type=(
                SyncJob.SyncType.INCREMENTAL
                if cfg.enable_incremental
                else SyncJob.SyncType.FULL
            ),
            status=SyncJob.SyncStatus.RUNNING,
            filemaker_layout=cfg.filemaker_layout,
            last_sync_timestamp=cfg.last_successful_sync,
            started_at=now,
        )

        try:
            rows = client.fetch(
                layout=cfg.filemaker_layout,
                fields=[
                    "AS400_NumberStripped",
                    "AS400_JobberPrice",
                ],
                where=cfg.filemaker_query,
            )

            job.records_fetched = len(rows)
            job.save(update_fields=["records_fetched"])

            existing = {
                p.part_number: p
                for p in Product.objects.filter(
                    part_number__in=[r["AS400_NumberStripped"] for r in rows]
                )
            }

            to_create, to_update = [], []

            for row in rows:
                mapped = apply_mapping(row, "PRODUCT")
                part_number = mapped["part_number"]

                mapped.setdefault("name", f"Product {part_number}")
                mapped.setdefault("slug", slugify(part_number))
                mapped.setdefault("category", default_category)
                mapped.setdefault("manufacturer", default_manufacturer)
                mapped["last_synced_at"] = now

                if part_number in existing:
                    obj = existing[part_number]
                    for field, value in mapped.items():
                        setattr(obj, field, value)
                    to_update.append(obj)
                else:
                    to_create.append(Product(**mapped))

            if to_create:
                Product.objects.bulk_create(
                    to_create,
                    batch_size=cfg.batch_size,
                )

            if to_update:
                Product.objects.bulk_update(
                    to_update,
                    fields=[
                        "name",
                        "slug",
                        "base_price",
                        "category",
                        "manufacturer",
                        "last_synced_at",
                    ],
                    batch_size=cfg.batch_size,
                )

            job.records_created = len(to_create)
            job.records_updated = len(to_update)
            job.status = SyncJob.SyncStatus.COMPLETED
            job.completed_at = timezone.now()
            job.save()

            cfg.last_successful_sync = job.completed_at
            cfg.save(update_fields=["last_successful_sync"])

            results.append(cfg.name)

        except Exception as exc:
            job.status = SyncJob.SyncStatus.FAILED
            job.error_message = str(exc)
            job.completed_at = timezone.now()
            job.save()
            raise

    return results

