import json
from pathlib import Path
from django.core.management.base import BaseCommand
from apps.autocare.models.base import AutocareRawRecord


def resolve_ref(swagger, ref):
    node = swagger
    for part in ref.lstrip("#/").split("/"):
        node = node[part]
    return node


class Command(BaseCommand):
    help = "Reconcile VCdb Swagger schema with raw payloads"

    def handle(self, *args, **options):
        swagger = json.load(open("data/autocare/swagger/vcdb.swagger.json"))
        out = {}

        for endpoint, path in swagger["paths"].items():
            if not endpoint.startswith("/api/v1/vcdb/"):
                continue

            schema = (
                path["get"]["responses"]["200"]
                ["content"]["application/json"]["schema"]
            )

            if "$ref" in schema:
                schema = resolve_ref(swagger, schema["$ref"])

            props = schema.get("properties", {})
            if not props:
                continue

            raw_endpoint = endpoint.replace("/api/v1", "")
            raw = AutocareRawRecord.objects.filter(endpoint=raw_endpoint).first()

            raw_fields = set()
            if raw and isinstance(raw.payload, list) and raw.payload:
                raw_fields = set(raw.payload[0].keys())

            fields = {}
            for name, spec in props.items():
                fields[name] = {
                    "type": spec.get("type"),
                    "format": spec.get("format"),
                    "nullable": spec.get("nullable", False),
                    "present_in_raw": name in raw_fields,
                }

            out[endpoint] = fields

        dest = Path("data/autocare/schema_reconciliation")
        dest.mkdir(parents=True, exist_ok=True)

        with open(dest / "vcdb.json", "w") as f:
            json.dump(out, f, indent=2)

        self.stdout.write(self.style.SUCCESS("VCdb schema reconciled"))
