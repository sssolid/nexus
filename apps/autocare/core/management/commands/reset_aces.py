from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Wipe all tables in schema autocare_aces and restart identities."

    def handle(self, *args, **kwargs):
        with connection.cursor() as cur:
            # Get all base tables in the autocare_aces schema
            cur.execute("""
                SELECT tablename
                FROM pg_tables
                WHERE schemaname = 'autocare_aces'
                ORDER BY tablename;
            """)
            tables = [r[0] for r in cur.fetchall()]

            if not tables:
                self.stdout.write(self.style.WARNING("No tables found in schema autocare_aces."))
                return

            fq = ", ".join([f'"autocare_aces"."{t}"' for t in tables])
            self.stdout.write(f"Truncating {len(tables)} tables in autocare_aces...")
            cur.execute(f"TRUNCATE TABLE {fq} RESTART IDENTITY CASCADE;")

        self.stdout.write(self.style.SUCCESS("autocare_aces wiped clean."))
