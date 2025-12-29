from django.db import models


class PIESReferenceFieldCode(models.Model):
    pies_reference_field_code_id = models.IntegerField(
        primary_key=True,
        db_column="PIESReferenceFieldCodeId",
    )

    pies_field = models.ForeignKey(
        "autocare_reference.PIESField",
        db_column="PIESFieldId",
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        related_name="reference_codes",
    )

    pies_code = models.ForeignKey(
        "autocare_reference.PIESCode",
        db_column="PIESCodeId",
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        related_name="reference_fields",
    )

    pies_expi_code_id = models.IntegerField(
        db_column="PIESExpiCodeId",
        blank=True,
        null=True,
    )

    reference_notes = models.TextField(
        db_column="ReferenceNotes",
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = '"autocare_reference"."pies_reference_field_code"'
        app_label = 'autocare_reference'
        verbose_name = "PIES Reference Field Code"
        verbose_name_plural = "PIES Reference Field Codes"
