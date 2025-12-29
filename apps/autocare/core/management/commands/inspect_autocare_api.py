import json
import time
import requests

from django.core.management.base import BaseCommand
from django.db.models import Max

from apps.autocare.api_client import AutocareAPIClient
from apps.autocare.pagination import extract_pagination
from apps.autocare.core.models import AutocareRawRecord


class Command(BaseCommand):
    help = "Inspect Autocare API responses (read-only) with correct pagination"

    def add_arguments(self, parser):
        parser.add_argument("endpoint", help="API endpoint path, e.g. /vcdb/Vehicle")
        parser.add_argument("--db", choices=["vcdb", "pcdb", "padb", "qdb"], default="vcdb")
        parser.add_argument("--asof", help="AsOfDate (YYYY-MM-DD)")
        parser.add_argument("--since", help="SinceDate (YYYY-MM-DD)")
        parser.add_argument("--pagesize", type=int, default=1000)
        parser.add_argument("--max-pages", type=int, default=10, help="Safety cap")
        parser.add_argument("--vehicle-id", type=int, help="Filter rows by VehicleID (client-side)")
        parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")

        # Debug / paging controls
        parser.add_argument("--start-page", type=int, help="Start from a specific page number")
        parser.add_argument(
            "--resume",
            action="store_true",
            help="Resume from last ingested raw page (uses AutocareRawRecord as a hint)",
        )
        parser.add_argument(
            "--skip-on-timeout",
            action="store_true",
            help="If a request times out, skip forward by incrementing pageNumber (only works when using pageNumber param).",
        )
        parser.add_argument("--sleep", type=float, default=0.0)

        # Output controls
        parser.add_argument(
            "--print-pagination",
            action="store_true",
            help="Print pagination info each page (currentPage/nextPageLink)",
        )
        parser.add_argument(
            "--dump-first",
            type=int,
            default=0,
            help="Dump first N rows of each page (after optional filtering). 0=off.",
        )

    def handle(self, *args, **opts):
        client = AutocareAPIClient()

        params = {"pageSize": opts["pagesize"]}
        if opts.get("since"):
            params["SinceDate"] = opts["since"]
        if opts.get("asof"):
            params["AsOfDate"] = opts["asof"]

        # ------------------------------------------------------------
        # Resume / Start page logic (optional, uses RAW table as hint)
        # ------------------------------------------------------------
        start_page = opts.get("start_page")

        if opts.get("resume"):
            # We use the raw table only as a convenience to avoid re-walking pages.
            # This does NOT write anything, it only reads max page_number.
            last_page = (
                AutocareRawRecord.objects.filter(
                    source_db=opts["db"],
                    endpoint=opts["endpoint"],
                    since_date=opts.get("since"),
                    as_of_date=opts.get("asof"),
                )
                .exclude(page_number__isnull=True)
                .aggregate(max_page=Max("page_number"))
                .get("max_page")
            )
            if last_page is not None:
                start_page = last_page + 1
                self.stdout.write(self.style.WARNING(f"Resuming from pageNumber={start_page}"))

        if start_page is not None:
            params["pageNumber"] = start_page

        next_url = opts["endpoint"]
        page_count = 0
        total_matches = 0

        while next_url and page_count < opts["max_pages"]:
            page_count += 1

            try:
                response = client.get(next_url, params=params)
            except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as exc:
                self.stderr.write(self.style.ERROR(f"Request failed: {exc.__class__.__name__}: {exc}"))

                # If we are driving paging via explicit pageNumber, we can skip forward.
                if opts["skip_on_timeout"] and params and "pageNumber" in params:
                    params["pageNumber"] += 1
                    self.stderr.write(self.style.WARNING(f"Skipping to pageNumber={params['pageNumber']}"))
                    time.sleep(max(opts["sleep"], 0.5))
                    continue

                # Otherwise we cannot safely guess the next page URL.
                break

            data = response.json()

            # ---- Use the SAME pagination function you already trust ----
            pagination = extract_pagination(response)
            page_number = pagination.get("currentPage") if pagination else None
            next_link = pagination.get("nextPageLink") if pagination else None

            if opts["print_pagination"]:
                self.stdout.write(
                    f"[page {page_count}] currentPage={page_number} nextPageLink={'YES' if next_link else 'NO'}"
                )

            # Autocare endpoints typically return a list at the top-level OR under a key.
            # We do not assume a schema; we search any list-y shape.
            rows = None
            if isinstance(data, list):
                rows = data
            elif isinstance(data, dict):
                # common patterns: {"data":[...]} or {"Data":[...]} or direct list-like under first list value
                if isinstance(data.get("data"), list):
                    rows = data["data"]
                elif isinstance(data.get("Data"), list):
                    rows = data["Data"]
                else:
                    # fallback: first list value in dict
                    for v in data.values():
                        if isinstance(v, list):
                            rows = v
                            break

            if rows is None:
                self.stderr.write(self.style.ERROR("Unexpected JSON shape: could not find list of rows"))
                if opts["pretty"]:
                    self.stderr.write(json.dumps(data, indent=2, default=str))
                else:
                    self.stderr.write(json.dumps(data, default=str))
                break

            # Filter by VehicleID if requested (client-side)
            if opts.get("vehicle_id") is not None:
                rows = [r for r in rows if isinstance(r, dict) and r.get("VehicleID") == opts["vehicle_id"]]

            if opts["dump_first"] and rows:
                to_dump = rows[: opts["dump_first"]]
                for r in to_dump:
                    self.stdout.write(json.dumps(r, indent=2 if opts["pretty"] else None, default=str))

            match_count = len(rows)
            total_matches += match_count

            self.stdout.write(
                self.style.SUCCESS(
                    f"Fetched page={page_number} rows={match_count} (total_matches={total_matches})"
                )
            )

            # Advance pagination
            if next_link:
                next_url = next_link
                params = None  # nextPageLink already contains parameters
            else:
                break

            if opts["sleep"]:
                time.sleep(opts["sleep"])

        self.stdout.write(self.style.SUCCESS(f"DONE. pages_visited={page_count} total_matches={total_matches}"))
