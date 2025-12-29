from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class PIESSegment(AutocareAPIMetadata, models.Model):
    id = models.BigAutoField(primary_key=True)

    pies_segment_id = models.IntegerField(
        db_column="PIESSegmentId",
        null=True,
        blank=True,
        db_index=True,
    )

    segment_abb = models.CharField(
        db_column="SegmentAbb",
        max_length=100,
    )

    segment_name = models.CharField(
        db_column="SegmentName",
        max_length=100,
    )

    segment_description = models.CharField(
        db_column="SegmentDescription",
        max_length=250,
    )

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = "autocare_pcdb"
        managed = True
        db_table = '"autocare_pcdb"."PIESSegment"'
        unique_together = [
            ("pies_segment_id", "segment_abb"),
        ]
        indexes = [
            models.Index(fields=["pies_segment_id"]),
        ]
