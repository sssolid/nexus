"""
Django management command to detect schema drift in VCdb (Vehicle Configuration Database).

This command compares two JSON schema snapshots:
- OLD: data/autocare/schema_snapshots/vcdb-latest.json (baseline/previous schema)
- NEW: data/autocare/schema_reconciliation/vcdb.json (current/updated schema)

For each API endpoint, it identifies:
- Added fields (present in new schema but not in old)
- Removed fields (present in old schema but not in new)

Usage:
    python manage.py detect_autocare_schema_drift

Output:
    - If drift detected: Displays endpoints with added/removed fields
    - If no drift: Success message confirming schema stability

This is typically run after ingesting new Autocare API data to ensure
backwards compatibility and catch breaking changes early.
"""

import json
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Detect schema drift between two VCdb schema snapshots.

    Compares field lists for each API endpoint between:
    - Baseline schema: data/autocare/schema_snapshots/vcdb-latest.json
    - Current schema: data/autocare/schema_reconciliation/vcdb.json

    Outputs:
        - WARNING with drift details if fields added/removed
        - SUCCESS if schemas are identical

    Example output:
        Schema drift detected:
        /api/v1.0/vehicles: +['newField'] -['oldField']
        /api/v1.0/makes: +['anotherField'] -[]
    """
    help = "Detect VCdb schema drift"

    def handle(self, *args, **options):
        """
        Execute schema drift detection.

        Loads both schema snapshots, compares field lists per endpoint,
        and reports any differences.

        Args:
            *args: Unused positional arguments from Django management command.
            **options: Unused keyword arguments from Django management command.

        Returns:
            None. Outputs results to stdout.

        Process:
            1. Load old (baseline) and new (current) schema JSON files
            2. Iterate through all endpoints in the new schema
            3. For each endpoint, calculate:
               - Added fields: in new but not in old
               - Removed fields: in old but not in new
            4. Collect drift information for endpoints with changes
            5. Output drift details or success message

        File paths:
            - Old schema: data/autocare/schema_snapshots/vcdb-latest.json
            - New schema: data/autocare/schema_reconciliation/vcdb.json
        """
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
