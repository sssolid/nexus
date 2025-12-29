from django.db import models


class PIESCode(models.Model):
    pies_code_id = models.IntegerField(
        primary_key=True,
        db_column="PIESCodeId",
    )

    code_value = models.CharField(
        max_length=255,
        db_column="CodeValue",
    )

    code_format = models.CharField(
        max_length=10,
        db_column="CodeFormat",
    )

    field_format = models.CharField(
        max_length=10,
        db_column="FieldFormat",
        blank=True,
        null=True,
    )

    code_description = models.CharField(
        max_length=255,
        db_column="CodeDescription",
    )

    source = models.CharField(
        max_length=255,
        db_column="Source",
    )

    class Meta:
        managed = True
        db_table = '"autocare_reference"."pies_code"'
        app_label = 'autocare_reference'
        verbose_name = "PIES Code"
        verbose_name_plural = "PIES Codes"

    def __str__(self):
        return f"{self.code_value} — {self.code_description}"


class AttachmentType(PIESCode):
    class Meta:
        proxy = True
        verbose_name = "Attachment Type"
        verbose_name_plural = "Attachment Types"
