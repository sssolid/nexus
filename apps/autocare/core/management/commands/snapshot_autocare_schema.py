import json
from pathlib import Path
from datetime import date
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Snapshot reconciled VCdb schema"

    def handle(self, *args, **options):
        src = Path("data/autocare/schema_reconciliation/vcdb.json")
        dest = Path("data/autocare/schema_snapshots")
        dest.mkdir(parents=True, exist_ok=True)

        today = date.today().isoformat()
        snap = dest / f"vcdb-{today}.json"

        data = json.load(open(src))
        with open(snap, "w") as f:
            json.dump(data, f, indent=2)

        (dest / "vcdb-latest.json").write_text(snap.read_text())

        self.stdout.write(self.style.SUCCESS(f"Snapshot saved: {snap.name}"))
