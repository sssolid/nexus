import json
import requests
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = "Fetch and cache VCdb Swagger schema"

    def handle(self, *args, **options):
        url = settings.VCDB_SWAGGER_URL
        dest = Path("data/autocare/swagger")
        dest.mkdir(parents=True, exist_ok=True)

        resp = requests.get(url, timeout=30)
        resp.raise_for_status()

        with open(dest / "vcdb.swagger.json", "w") as f:
            json.dump(resp.json(), f, indent=2)

        self.stdout.write(self.style.SUCCESS("VCdb Swagger cached"))
