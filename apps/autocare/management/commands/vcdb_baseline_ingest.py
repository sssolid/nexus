import time
import subprocess
from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import now

from apps.autocare.vcdb.plan import (
    VCDB_BASELINE_PLAN,
    VCDB_BASELINE_AS_OF,
    DEFAULT_PAGE_SIZE,
)
from apps.autocare.models.vcdb_ingest_state import VCDBIngestState


class Command(BaseCommand):
    help = "Run full VCDB baseline ingest with retries and resume support"

    def add_arguments(self, parser):
        parser.add_argument("--resume", action="store_true")
        parser.add_argument("--retries", type=int, default=3)
        parser.add_argument("--sleep", type=float, default=0.5)

    def handle(self, *args, **opts):
        retries = opts["retries"]
        sleep = opts["sleep"]

        completed = set(
            VCDBIngestState.objects
            .filter(as_of_date=VCDB_BASELINE_AS_OF)
            .values_list("endpoint", flat=True)
        ) if opts["resume"] else set()

        for endpoint in VCDB_BASELINE_PLAN:
            if endpoint in completed:
                self.stdout.write(f"✓ Skipping {endpoint} (already completed)")
                continue

            self.stdout.write(f"▶ Ingesting {endpoint}")

            for attempt in range(1, retries + 1):
                try:
                    subprocess.run(
                        [
                            "python",
                            "manage.py",
                            "ingest_autocare",
                            "--db", "vcdb",
                            endpoint,
                            "--asof", VCDB_BASELINE_AS_OF,
                            "--pagesize", str(DEFAULT_PAGE_SIZE),
                        ],
                        check=True,
                    )

                    VCDBIngestState.objects.create(
                        endpoint=endpoint,
                        as_of_date=VCDB_BASELINE_AS_OF,
                    )

                    self.stdout.write(f"✔ Completed {endpoint}")
                    break

                except subprocess.CalledProcessError as e:
                    self.stderr.write(
                        f"✖ Attempt {attempt}/{retries} failed for {endpoint}"
                    )
                    if attempt == retries:
                        raise CommandError(
                            f"Baseline ingest FAILED at {endpoint}"
                        )
                    time.sleep(5)

            time.sleep(sleep)

        self.stdout.write(
            self.style.SUCCESS(
                "✔ VCDB BASELINE INGEST COMPLETE"
            )
        )
