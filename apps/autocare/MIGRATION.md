ALTER TABLE autocare_autocarerawrecord
ADD COLUMN request_path varchar(255);

UPDATE autocare_autocarerawrecord
SET request_path = '/api/v1' || endpoint
WHERE request_path IS NULL;

UPDATE autocare_autocarerawrecord
SET endpoint =
    source_db || ':' || split_part(endpoint, '/', 3);

ALTER TABLE autocare_autocarerawrecord
ALTER COLUMN request_path SET NOT NULL;

CREATE INDEX idx_autocare_raw_endpoint
ON autocare_autocarerawrecord (source_db, endpoint);

CREATE INDEX idx_autocare_raw_request_path
ON autocare_autocarerawrecord (source_db, request_path);


Update django model...

class AutocareRawRecord(models.Model):
    source_db = models.CharField(max_length=16)

    # Logical identifier (stable)
    endpoint = models.CharField(
        max_length=128,
        help_text="Logical endpoint (e.g. vcdb:Vehicle)"
    )

    # Actual API path used
    request_path = models.CharField(
        max_length=255,
        help_text="Actual API path used (e.g. /api/v1/vcdb/Vehicle)"
    )

    fetched_at = models.DateTimeField(auto_now_add=True)

    since_date = models.DateField(null=True, blank=True)
    as_of_date = models.DateField(null=True, blank=True)

    page_number = models.IntegerField(null=True, blank=True)
    page_size = models.IntegerField(null=True, blank=True)

    http_status = models.IntegerField()
    record_count = models.IntegerField()
    payload = models.JSONField()
    ingestion_mode = models.CharField(max_length=16)
