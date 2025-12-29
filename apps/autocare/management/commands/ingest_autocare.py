import time
import requests

from django.core.management.base import BaseCommand, CommandError

from apps.autocare.api_client import AutocareAPIClient
from apps.autocare.core.models import AutocareRawRecord
from apps.autocare.pagination import extract_pagination
from apps.autocare.utils import get_record_count
from apps.autocare.ingest.plans import EndpointSpec


class Command(BaseCommand):
    help = "Ingest an Autocare API endpoint into raw storage (spec-driven, resumable)"

    def add_arguments(self, parser):
        parser.add_argument(
            "endpoint",
            nargs="?",
            help="Legacy endpoint path, e.g. /vcdb/Vehicle or /api/v1/vcdb/Vehicle (deprecated)",
        )
        parser.add_argument(
            "--db",
            required=True,
            choices=["vcdb", "pcdb", "padb", "qdb", "brand"],
        )
        parser.add_argument("--resource", help="Resource name, e.g. Vehicle")
        parser.add_argument("--api-version", help="API version, e.g. v1 or v4")
        parser.add_argument("--since", default=None)
        parser.add_argument("--asof", default=None)
        parser.add_argument("--pagesize", type=int, default=1000)
        parser.add_argument("--mode", choices=["debug", "full", "incremental"], default="full")
        parser.add_argument("--start-page", type=int)
        parser.add_argument("--resume", action="store_true")

    # ============================================================
    # EndpointSpec resolution
    # ============================================================

    def _resolve_spec(self, options) -> EndpointSpec:
        endpoint = options.get("endpoint")
        db = options["db"]
        resource = options.get("resource")
        api_version = options.get("api_version")

        if resource and api_version:
            return EndpointSpec(db=db, resource=resource, api_version=api_version)

        if not endpoint:
            raise CommandError("You must provide either endpoint or (--resource and --api-version).")

        parts = endpoint.strip("/").split("/")

        if parts[0] == "api":
            api_version, db, resource = parts[1:4]
        else:
            db, resource = parts[:2]
            api_version = "v1"

        return EndpointSpec(db=db, resource=resource, api_version=api_version)

    # ============================================================
    # Main
    # ============================================================

    def handle(self, *args, **options):
        spec = self._resolve_spec(options)
        client = AutocareAPIClient(spec.db)

        params = {"pageSize": options["pagesize"]}

        if options["since"]:
            params["SinceDate"] = options["since"]
        if options["asof"]:
            params["AsOfDate"] = options["asof"]

        # --------------------------------------------------------
        # Resume logic
        # --------------------------------------------------------
        start_page = options.get("start_page")

        if options["resume"]:
            last_page = (
                AutocareRawRecord.objects.filter(
                    source_db=spec.db,
                    endpoint_key=spec.key,
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
                self.stdout.write(self.style.WARNING(f"Resuming from page {start_page}"))

        if start_page:
            params["pageNumber"] = start_page

        next_url = spec.request_path

        # --------------------------------------------------------
        # Main ingest loop
        # --------------------------------------------------------
        while next_url:
            try:
                response = client.get(next_url, params=params)
            except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as exc:
                page = params.get("pageNumber") if params else None
                self.stderr.write(self.style.ERROR(f"⚠ Request failed on page {page} — skipping"))

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
                source_db=spec.db,
                endpoint_key=spec.key,
                since_date=options["since"],
                as_of_date=options["asof"],
                page_number=page_number,
            ).exists()

            if exists:
                self.stdout.write(self.style.WARNING(f"Skipping duplicate page {page_number}"))
            else:
                AutocareRawRecord.objects.create(
                    source_db=spec.db,
                    endpoint_key=spec.key,
                    request_path=spec.request_path,
                    since_date=options["since"],
                    as_of_date=options["asof"],
                    page_number=page_number,
                    page_size=page_size,
                    http_status=response.status_code,
                    record_count=get_record_count(data),
                    payload=data,
                    ingestion_mode=options["mode"],
                )
                self.stdout.write(self.style.SUCCESS(f"Page {page_number} ingested"))

            # ----------------------------------------------------
            # Pagination advance
            # ----------------------------------------------------
            if pagination and pagination.get("nextPageLink"):
                next_url = pagination["nextPageLink"]
                params = None
            else:
                break

            time.sleep(0.5)
