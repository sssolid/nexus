import json
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Detect VCdb schema drift"

    def handle(self, *args, **options):
        old = json.load(open("data/autocare/schema_snapshots/vcdb-latest.json"))
        new = json.load(open("data/autocare/schema_reconciliation/vcdb.json"))

        drift = {}

        for endpoint, fields in new.items():
            old_fields = old.get(endpoint, {})
            added = set(fields) - set(old_fields)
            removed = set(old_fields) - set(fields)

            if added or removed:
                drift[endpoint] = {
                    "added": sorted(added),
                    "removed": sorted(removed),
                }

        if drift:
            self.stdout.write(self.style.WARNING("Schema drift detected:"))
            for ep, d in drift.items():
                self.stdout.write(f"{ep}: +{d['added']} -{d['removed']}")
        else:
            self.stdout.write(self.style.SUCCESS("No schema drift detected"))
