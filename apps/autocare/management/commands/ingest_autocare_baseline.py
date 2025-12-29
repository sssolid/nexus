import time
import subprocess
from django.core.management.base import BaseCommand, CommandError

from apps.autocare.ingest.plans import get_dataset, DEFAULT_PAGE_SIZE
from apps.autocare.models.shared.ingest_state import IngestState


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--db", required=True)
        parser.add_argument("--asof", default=None)
        parser.add_argument("--resume", action="store_true")
        parser.add_argument("--retries", type=int, default=3)
        parser.add_argument("--sleep", type=float, default=0.5)

    def handle(self, *args, **opts):
        dataset_name = opts["db"]
        dataset = get_dataset(dataset_name)

        as_of = opts["asof"] or dataset.default_as_of
        if dataset.supports_as_of and not as_of:
            raise CommandError(f"{dataset_name} requires --asof (or set default_as_of).")

        completed = set()
        if opts["resume"]:
            completed = set(
                IngestState.objects.filter(
                    dataset=dataset_name,
                    as_of_date=as_of,
                ).values_list("endpoint_key", flat=True)
            )

        for spec in dataset.plan:
            if spec.key in completed:
                self.stdout.write(f"✓ Skipping {spec.key}")
                continue

            for attempt in range(1, opts["retries"] + 1):
                try:
                    cmd = [
                        "python", "manage.py", "ingest_autocare",
                        "--db", dataset_name,
                        "--resource", spec.resource,
                        "--api-version", spec.api_version,
                        "--pagesize", str(DEFAULT_PAGE_SIZE),
                    ]
                    if dataset.supports_as_of:
                        cmd += ["--asof", str(as_of)]
                    if opts["resume"]:
                        cmd.append("--resume")

                    subprocess.run(cmd, check=True)

                    IngestState.objects.get_or_create(
                        dataset=dataset_name,
                        endpoint_key=spec.key,
                        as_of_date=as_of,
                    )
                    break

                except subprocess.CalledProcessError:
                    if attempt == opts["retries"]:
                        raise CommandError(f"FAILED at {spec.key}")
                    time.sleep(5)

            time.sleep(opts["sleep"])
