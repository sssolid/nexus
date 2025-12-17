import time
import requests

from django.core.management.base import BaseCommand

from apps.autocare.api import AutocareAPIClient
from apps.autocare.models.base import AutocareRawRecord
from apps.autocare.pagination import extract_pagination
from apps.autocare.utils import get_record_count


class Command(BaseCommand):
    help = "Ingest an Autocare API endpoint into raw storage (resumable)"

    def add_arguments(self, parser):
        parser.add_argument(
            "endpoint",
            help="API endpoint path, e.g. /vcdb/Vehicle",
        )
        parser.add_argument(
            "--db",
            required=True,
            choices=["vcdb", "pcdb", "padb", "qdb"],
            help="Autocare source database",
        )
        parser.add_argument(
            "--since",
            help="SinceDate (YYYY-MM-DD)",
            default=None,
        )
        parser.add_argument(
            "--asof",
            help="AsOfDate (YYYY-MM-DD)",
            default=None,
        )
        parser.add_argument(
            "--pagesize",
            type=int,
            default=1000,
        )
        parser.add_argument(
            "--mode",
            choices=["debug", "full", "incremental"],
            default="full",
        )
        parser.add_argument(
            "--start-page",
            type=int,
            help="Start ingesting from a specific page number",
        )
        parser.add_argument(
            "--resume",
            action="store_true",
            help="Resume from last successfully ingested page",
        )

    def handle(self, *args, **options):
        client = AutocareAPIClient()

        params = {
            "pageSize": options["pagesize"],
        }

        if options["since"]:
            params["SinceDate"] = options["since"]

        if options["asof"]:
            params["AsOfDate"] = options["asof"]

        # ------------------------------------------------------------
        # Resume / Start-page logic
        # ------------------------------------------------------------
        start_page = options.get("start_page")

        if options.get("resume"):
            last_page = (
                AutocareRawRecord.objects
                .filter(
                    source_db=options["db"],
                    endpoint=options["endpoint"],
                    since_date=options["since"],
                    as_of_date=options["asof"],
                )
                .exclude(page_number__isnull=True)
                .order_by("-page_number")
                .values_list("page_number", flat=True)
                .first()
            )

            if last_page is not None:
                start_page = last_page + 1
                self.stdout.write(
                    self.style.WARNING(
                        f"Resuming from page {start_page}"
                    )
                )

        if start_page:
            params["pageNumber"] = start_page

        next_url = options["endpoint"]

        # ------------------------------------------------------------
        # Main ingest loop
        # ------------------------------------------------------------
        while next_url:
            try:
                response = client.get(next_url, params=params)
            except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as exc:
                page = params.get("pageNumber") if params else None
                self.stderr.write(
                    self.style.ERROR(
                        f"⚠ Request failed on page {page} — skipping ({exc.__class__.__name__})"
                    )
                )

                # Skip forward safely
                if params and "pageNumber" in params:
                    params["pageNumber"] += 1
                    time.sleep(1)
                    continue

                break

            data = response.json()
            pagination = extract_pagination(response)

            page_number = pagination.get("currentPage") if pagination else None
            page_size = pagination.get("pageSize") if pagination else None

            exists = AutocareRawRecord.objects.filter(
                source_db=options["db"],
                endpoint=options["endpoint"],
                since_date=options["since"],
                as_of_date=options["asof"],
                page_number=page_number,
            ).exists()

            if exists:
                self.stdout.write(
                    self.style.WARNING(
                        f"Skipping duplicate page {page_number}"
                    )
                )
            else:
                AutocareRawRecord.objects.create(
                    source_db=options["db"],
                    endpoint=options["endpoint"],
                    since_date=options["since"],
                    as_of_date=options["asof"],
                    page_number=page_number,
                    page_size=page_size,
                    http_status=response.status_code,
                    record_count=get_record_count(data),
                    payload=data,
                    ingestion_mode=options["mode"],
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Page {page_number} ingested"
                    )
                )

            # --------------------------------------------------------
            # Advance pagination
            # --------------------------------------------------------
            if pagination and pagination.get("nextPageLink"):
                next_url = pagination["nextPageLink"]
                params = None  # nextPageLink already contains params
            else:
                break

            time.sleep(0.5)
