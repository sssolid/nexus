"""
Django management command for ACES file ingestion.

Usage:
    python manage.py ingest_aces /path/to/aces_file.xml
    python manage.py ingest_aces /path/to/aces_file.xml --verify
    python manage.py ingest_aces /path/to/aces_file.xml --batch-size 10000
"""

from django.core.management.base import BaseCommand, CommandError
import os

from apps.autocare.management.commands.verify_aces import verify_aces_integrity
from apps.data_sync.services.aces_ingest import ingest_aces_file
from apps.data_sync.utils.db_silence import silence_db_debug


class Command(BaseCommand):
    help = 'Ingest ACES XML file into database with zero data loss'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path',
            type=str,
            help='Path to ACES XML file'
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=5000,
            help='Batch size for bulk inserts (default: 5000)'
        )
        parser.add_argument(
            '--verify',
            action='store_true',
            help='Run integrity verification after ingestion'
        )
        parser.add_argument(
            '--no-transaction',
            action='store_true',
            help='Disable atomic transaction (not recommended)'
        )

    def handle(self, *args, **options):
        file_path = options['file_path']
        batch_size = options['batch_size']
        verify = options['verify']

        # Validate file exists
        if not os.path.exists(file_path):
            raise CommandError(f'File not found: {file_path}')

        if not file_path.lower().endswith('.xml'):
            self.stdout.write(
                self.style.WARNING(
                    f'Warning: File does not have .xml extension: {file_path}'
                )
            )

        # Run ingestion
        self.stdout.write(
            self.style.SUCCESS(f'\nStarting ACES ingestion from: {file_path}')
        )

        try:
            with silence_db_debug():
                stats = ingest_aces_file(
                    path=file_path,
                    stdout=self.stdout,
                    batch_size=batch_size
                )

            self.stdout.write(
                self.style.SUCCESS('\n✓ Ingestion completed successfully!')
            )

            # Run verification if requested
            if verify:
                self.stdout.write('\nRunning integrity verification...')
                results = verify_aces_integrity(file_path, verbose=True)

                if results['issues']:
                    self.stdout.write(
                        self.style.ERROR(
                            f'\n⚠ Verification found {len(results["issues"])} issues!'
                        )
                    )
                    for issue in results['issues']:
                        self.stdout.write(self.style.ERROR(f'  • {issue}'))
                else:
                    self.stdout.write(
                        self.style.SUCCESS('\n✓ Verification passed - no issues found!')
                    )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'\n✗ Ingestion failed: {str(e)}')
            )
            raise CommandError(f'Ingestion failed: {str(e)}')