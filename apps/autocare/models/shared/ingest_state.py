# apps/autocare/models/shared/ingest_state.py
from django.db import models

class IngestState(models.Model):
    dataset = models.CharField(max_length=10, db_index=True)        # vcdb/pcdb/padb/qdb
    endpoint_key = models.CharField(max_length=120, db_index=True)  # padb:MeasurementGroup
    as_of_date = models.DateField(db_index=True)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = '"autocare_shared"."ingest_state"'
        managed = False

