from django.db import models


class AutocareTemporalModel(models.Model):
    # These columns are consistent in the API/schema payloads
    culture_id = models.CharField(max_length=10, db_index=True, db_column="CultureID")
    effective_date = models.DateTimeField(db_index=True, db_column="EffectiveDateTime")
    end_date = models.DateTimeField(null=True, blank=True, db_column="EndDateTime")

    class Meta:
        abstract = True


class AutocareNamedModel(AutocareTemporalModel):
    # Do NOT set db_column here; different tables use different "*Name" columns.
    name = models.CharField(max_length=255, db_index=True)

    class Meta:
        abstract = True


class AutocareRawRecord(models.Model):
    SOURCE_CHOICES = [
        ("vcdb", "VCdb"),
        ("pcdb", "PCdb"),
        ("padb", "PAdb"),
        ("qdb", "Qdb"),
    ]

    source_db = models.CharField(max_length=10, choices=SOURCE_CHOICES)

    endpoint_key = models.CharField(max_length=120, db_index=True)
    request_path = models.CharField(max_length=255)

    fetched_at = models.DateTimeField(auto_now_add=True)
    as_of_date = models.CharField(max_length=20, null=True, blank=True)
    since_date = models.CharField(max_length=20, null=True, blank=True)

    page_number = models.IntegerField(null=True, blank=True)
    page_size = models.IntegerField(null=True, blank=True)

    http_status = models.IntegerField()
    record_count = models.IntegerField(null=True, blank=True)

    payload = models.JSONField()

    ingestion_mode = models.CharField(
        max_length=20,
        choices=[
            ("debug", "Debug"),
            ("full", "Full"),
            ("incremental", "Incremental"),
        ],
        default="full",
    )

    class Meta:
        db_table = "autocare_autocarerawrecord"
        indexes = [
            models.Index(fields=["source_db", "endpoint_key"]),
            models.Index(fields=["fetched_at"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "source_db",
                    "endpoint_key",
                    "since_date",
                    "as_of_date",
                    "page_number",
                    "page_size",
                ],
                name="unique_autocare_ingest_page",
            )
        ]

    def __str__(self):
        return f"{self.endpoint_key} page={self.page_number}"
