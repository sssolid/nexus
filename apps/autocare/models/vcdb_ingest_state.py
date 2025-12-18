# apps/autocare/models/vcdb_ingest_state.py
from django.db import models

class VCDBIngestState(models.Model):
    endpoint = models.CharField(max_length=255, unique=True)
    as_of_date = models.DateField()
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = '"autocare_vcdb"."ingest_state"'
