from django.db import models


class PIESField(models.Model):
    pies_field_id = models.IntegerField(
        primary_key=True,
        db_column="PIESFieldId",
    )

    field_name = models.CharField(
        max_length=100,
        db_column="FieldName",
    )

    reference_field_number = models.CharField(
        db_column="ReferenceFieldNumber",
        max_length=10,
    )

    pies_segment_id = models.IntegerField(
        db_column="PIESSegmentId",
    )

    class Meta:
        managed = True
        db_table = '"autocare_reference"."pies_field"'
        app_label = 'autocare_reference'
        verbose_name = "PIES Field"
        verbose_name_plural = "PIES Fields"

    def __str__(self):
        return f"{self.field_name} (FieldId={self.pies_field_id})"
