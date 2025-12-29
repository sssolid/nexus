from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class PIESField(AutocareAPIMetadata, models.Model):
    id = models.BigAutoField(primary_key=True)

    pies_field_id = models.IntegerField(
        db_column="PIESFieldId",
        null=True,
        blank=True,
        db_index=True,
    )

    field_name = models.CharField(
        db_column="FieldName",
        max_length=500,
    )

    reference_field_number = models.CharField(
        db_column="ReferenceFieldNumber",
        max_length=500,
    )

    pies_segment_id = models.IntegerField(
        db_column="PIESSegmentId",
        null=True,
        blank=True,
        db_index=True,
    )

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = "autocare_pcdb"
        managed = True
        db_table = '"autocare_pcdb"."PIESField"'
        unique_together = [
            ("pies_field_id", "reference_field_number"),
        ]
        indexes = [
            models.Index(fields=["pies_field_id"]),
            models.Index(fields=["pies_segment_id"]),
        ]
        verbose_name = "PIES Field"
        verbose_name_plural = "PIES Fields"
