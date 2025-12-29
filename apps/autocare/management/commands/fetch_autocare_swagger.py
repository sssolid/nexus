"""
A custom Django management command to fetch and cache Autocare Swagger schemas.

This module contains a management command which downloads Autocare Swagger
schemas from a configured URL and caches them locally as formatted JSON files.
It ensures directory creation if required and provides success feedback upon
completion.

Classes:
    Command: Implements the custom management command to handle caching of
    the Swagger schema.
"""

import json
import requests
import filecmp
import shutil
from datetime import datetime
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = "Fetch and cache Autocare Swagger schema"

    def add_arguments(self, parser):
        """
        Add custom command line arguments.

        Args:
            parser: ArgumentParser instance to add arguments to
        """
        parser.add_argument(
            '--db',
            type=str,
            choices=['vcdb', 'pcdb', 'qdb'],
            default='vcdb',
            help='Database to fetch Swagger schema for (vcdb, pcdb, or qdb)'
        )

    def handle(self, *args, **options):
        """
        Execute the command to fetch and cache the Autocare Swagger schema.

        Downloads the schema from a configured Swagger URL and saves it as
        formatted JSON to the appropriate data directory.

        Args:
            *args: Positional arguments (unused)
            **options: Command options, including:
                db (str): The database to fetch ('vcdb', 'pcdb', or 'qdb')

        Raises:
            requests.HTTPError: If the HTTP request fails
            requests.Timeout: If the request times out (30s timeout)
            json.JSONDecodeError: If the response is not valid JSON

        Returns:
            None: Outputs success message to stdout on completion
        """
        database = options['db']

        url_mapping = {
            'vcdb': settings.VCDB_SWAGGER_URL,
            'pcdb': settings.PCDB_SWAGGER_URL,
            'qdb': settings.QDB_SWAGGER_URL,
        }

        url = url_mapping[database]
        dest = Path("data/autocare/swagger")
        dest.mkdir(parents=True, exist_ok=True)

        resp = requests.get(url, timeout=30)
        resp.raise_for_status()

        # Generate date-based filename
        date_str = datetime.now().strftime("%Y-%m-%d")
        dated_filename = dest / f"{date_str}-{database}.swagger.json"
        latest_filename = dest / f"{database}.swagger.latest.json"

        # Write downloaded content to dated file
        with open(dated_filename, "w") as f:
            json.dump(resp.json(), f, indent=2)

        # Check if latest file exists and compare
        should_update = True
        if latest_filename.exists():
            if filecmp.cmp(dated_filename, latest_filename, shallow=False):
                should_update = False
                self.stdout.write(
                    self.style.WARNING(
                        f"{database.upper()} Swagger schema unchanged, skipping update"
                    )
                )

        # Copy to latest if different or doesn't exist
        if should_update:
            shutil.copy2(dated_filename, latest_filename)
            self.stdout.write(
                self.style.SUCCESS(
                    f"{database.upper()} Swagger schema cached to {latest_filename.name}"
                )
            )
