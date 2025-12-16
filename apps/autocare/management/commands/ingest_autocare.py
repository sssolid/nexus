import time

from django.core.management.base import BaseCommand

from apps.autocare.api import AutocareAPIClient
from apps.autocare.models.base import AutocareRawRecord
from apps.autocare.pagination import extract_pagination
from apps.autocare.utils import get_record_count


class Command(BaseCommand):
    help = "Ingest an Autocare API endpoint into raw storage"

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

    def handle(self, *args, **options):
        client = AutocareAPIClient()

        params = {
            "pageSize": options["pagesize"],
        }

        if options["since"]:
            params["SinceDate"] = options["since"]
        if options["asof"]:
            params["AsOfDate"] = options["asof"]

        next_url = options["endpoint"]

        while next_url:
            response = client.get(next_url, params=params)
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

            next_url = pagination.get("nextPageLink") if pagination else None
            params = None  # nextPageLink already includes parameters

            time.sleep(0.5)