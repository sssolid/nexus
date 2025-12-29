from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "TRUNCATE all tables in a schema (dev reset, FK-safe)."

    def add_arguments(self, parser):
        parser.add_argument("--schema", default="autocare_vcdb")

    def handle(self, *args, **opts):
        schema = opts["schema"]

        with connection.cursor() as cursor:
            # Fetch table names safely
            cursor.execute(
                """
                SELECT tablename
                FROM pg_tables
                WHERE schemaname = %s
                ORDER BY tablename;
                """,
                [schema],
            )
            tables = [row[0] for row in cursor.fetchall()]

            if not tables:
                self.stdout.write(self.style.WARNING(f"No tables found in schema '{schema}'."))
                return

            self.stdout.write(f"Truncating {len(tables)} tables in schema '{schema}'...")

            # Truncate each table explicitly (psycopg-safe)
            for table in tables:
                sql = f'TRUNCATE TABLE "{schema}"."{table}" RESTART IDENTITY CASCADE;'
                cursor.execute(sql)

        self.stdout.write(self.style.SUCCESS(f"Schema '{schema}' truncated successfully."))
