"""
Celery tasks for exports application.
"""

from datetime import timedelta

from celery import shared_task
from django.utils import timezone


@shared_task
def process_scheduled_exports():
    """
    Process scheduled export jobs that are due.
    Runs every 15 minutes via Celery Beat.
    """
    from .models import ExportJob, ScheduledExport

    now = timezone.now()

    # Get exports that are due
    due_exports = ScheduledExport.objects.filter(is_active=True, next_run_at__lte=now)

    processed = 0
    for scheduled_export in due_exports:
        # Create export job
        job = ExportJob.objects.create(
            user=scheduled_export.user,
            template=scheduled_export.template,
            name=f"{scheduled_export.name} - Automated",
            format=scheduled_export.template.format,
            status="PENDING",
        )

        # Trigger export processing
        process_export_job.delay(job.id)

        # Update next run time based on frequency
        if scheduled_export.frequency == "DAILY":
            scheduled_export.next_run_at = now + timedelta(days=1)
        elif scheduled_export.frequency == "WEEKLY":
            scheduled_export.next_run_at = now + timedelta(weeks=1)
        elif scheduled_export.frequency == "MONTHLY":
            scheduled_export.next_run_at = now + timedelta(days=30)

        scheduled_export.last_run_at = now
        scheduled_export.save()

        processed += 1

    return f"Processed {processed} scheduled exports"


@shared_task
def process_export_job(job_id):
    """
    Process an individual export job.
    """
    import csv
    import io

    from django.core.files.base import ContentFile

    from apps.products.models import Product

    from .models import ExportJob

    try:
        job = ExportJob.objects.get(id=job_id)
        job.status = "PROCESSING"
        job.started_at = timezone.now()
        job.save()

        # Get products to export
        products = Product.objects.filter(is_active=True).select_related(
            "category", "manufacturer"
        )

        # Create CSV export (simplified example)
        output = io.StringIO()
        writer = csv.writer(output)

        # Header
        writer.writerow(["Part Number", "Name", "Manufacturer", "Price", "Stock"])

        # Data
        for product in products.iterator(chunk_size=100):
            writer.writerow(
                [
                    product.part_number,
                    product.name,
                    product.manufacturer.name,
                    str(product.base_price),
                    product.quantity_in_stock,
                ]
            )
            job.processed_records += 1

        job.total_records = job.processed_records

        # Save file
        filename = f"export_{job_id}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.csv"
        job.file.save(filename, ContentFile(output.getvalue().encode("utf-8")))

        job.status = "COMPLETED"
        job.completed_at = timezone.now()
        job.save()

        return f"Export job {job_id} completed successfully"

    except Exception as e:
        job.status = "FAILED"
        job.error_message = str(e)
        job.completed_at = timezone.now()
        job.save()
        raise


@shared_task
def cleanup_old_exports():
    """
    Delete export files older than 30 days.
    Runs daily at 2 AM.
    """
    from .models import ExportJob

    cutoff_date = timezone.now() - timedelta(days=30)

    old_exports = ExportJob.objects.filter(
        created_at__lt=cutoff_date, status__in=["COMPLETED", "FAILED"]
    )

    count = 0
    for export_job in old_exports:
        if export_job.file:
            export_job.file.delete()
        export_job.delete()
        count += 1

    return f"Cleaned up {count} old export files"


@shared_task
def send_export_notification(job_id):
    """
    Send email notification when export is complete.
    """
    from django.core.mail import send_mail

    from .models import ExportJob

    try:
        job = ExportJob.objects.get(id=job_id)

        if job.status == "COMPLETED":
            subject = f"Export Ready: {job.name}"
            message = f'Your export "{job.name}" is ready for download.'

            send_mail(
                subject,
                message,
                "noreply@nexus.com",
                [job.user.email],
                fail_silently=True,
            )

            return f"Notification sent to {job.user.email}"
    except Exception as e:
        return f"Failed to send notification: {str(e)}"
