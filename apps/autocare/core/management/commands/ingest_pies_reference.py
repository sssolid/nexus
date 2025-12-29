# from django.core.management.base import BaseCommand
# from django.db import connections, transaction
#
# from apps.autocare.models.reference import (
#     PIESCode,
#     PIESField,
#     PIESReferenceFieldCode,
# )
#
#
# class Command(BaseCommand):
#     help = "Ingest PIES reference tables from MySQL into Postgres"
#
#     def handle(self, *args, **options):
#         mysql_pcadb = connections["mysql_autocare_pcadb"]
#
#         self.stdout.write("Ingesting PIESCode...")
#         self.ingest_pies_code(mysql_pcadb)
#
#         self.stdout.write("Ingesting PIESField...")
#         self.ingest_pies_field(mysql_pcadb)
#
#         self.stdout.write("Ingesting PIESReferenceFieldCode...")
#         self.ingest_reference_field_code(mysql_pcadb)
#
#         self.stdout.write(self.style.SUCCESS("PIES reference ingest complete"))
#
#     def ingest_pies_code(self, mysql):
#         with mysql.cursor() as cursor:
#             cursor.execute("""
#                 SELECT
#                     PIESCodeId,
#                     CodeValue,
#                     CodeFormat,
#                     FieldFormat,
#                     CodeDescription,
#                     Source
#                 FROM PIESCode
#             """)
#             rows = cursor.fetchall()
#
#         with transaction.atomic():
#             for row in rows:
#                 PIESCode.objects.update_or_create(
#                     pies_code_id=row[0],
#                     defaults={
#                         "code_value": row[1],
#                         "code_format": row[2],
#                         "field_format": row[3],
#                         "code_description": row[4],
#                         "source": row[5],
#                     },
#                 )
#
#     def ingest_pies_field(self, mysql):
#         with mysql.cursor() as cursor:
#             cursor.execute("""
#                 SELECT
#                     PIESFieldId,
#                     FieldName,
#                     ReferenceFieldNumber,
#                     PIESSegmentId
#                 FROM PIESField
#             """)
#             rows = cursor.fetchall()
#
#         with transaction.atomic():
#             for row in rows:
#                 PIESField.objects.update_or_create(
#                     pies_field_id=row[0],
#                     defaults={
#                         "field_name": row[1],
#                         "reference_field_number": row[2],
#                         "pies_segment_id": row[3],
#                     },
#                 )
#
#     def ingest_reference_field_code(self, mysql):
#         with mysql.cursor() as cursor:
#             cursor.execute("""
#                 SELECT
#                     PIESReferenceFieldCodeId,
#                     PIESFieldId,
#                     PIESCodeId,
#                     PIESExpiCodeId,
#                     ReferenceNotes
#                 FROM PIESReferenceFieldCode
#             """)
#             rows = cursor.fetchall()
#
#         with transaction.atomic():
#             for row in rows:
#                 PIESReferenceFieldCode.objects.update_or_create(
#                     pies_reference_field_code_id=row[0],
#                     defaults={
#                         "pies_field_id": row[1],
#                         "pies_code_id": row[2],
#                         "pies_expi_code_id": row[3],
#                         "reference_notes": row[4],
#                     },
#                 )
