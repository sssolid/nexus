from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class PIESReferenceFieldCode(AutocareAPIMetadata, models.Model):
    id = models.BigAutoField(primary_key=True)

    pies_reference_field_code_id = models.IntegerField(
        db_column="PIESReferenceFieldCodeId",
        null=True,
        blank=True,
        db_index=True,
    )

    pies_field_id = models.IntegerField(
        db_column="PIESFieldId",
        null=True,
        blank=True,
        db_index=True,
    )

    pies_code_id = models.IntegerField(
        db_column="PIESCodeId",
        null=True,
        blank=True,
        db_index=True,
    )

    pies_expi_code_id = models.IntegerField(
        db_column="PIESExpiCodeId",
        null=True,
        blank=True,
        db_index=True,
    )

    reference_notes = models.CharField(
        db_column="ReferenceNotes",
        max_length=2000,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = "autocare_pcdb"
        managed = True
        db_table = '"autocare_pcdb"."PIESReferenceFieldCode"'
        unique_together = [
            ("pies_reference_field_code_id", "pies_field_id", "pies_code_id", "pies_expi_code_id"),
        ]
        indexes = [
            models.Index(fields=["pies_reference_field_code_id"]),
            models.Index(fields=["pies_field_id"]),
            models.Index(fields=["pies_code_id"]),
            models.Index(fields=["pies_expi_code_id"]),
        ]
