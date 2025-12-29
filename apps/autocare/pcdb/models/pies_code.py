from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class PIESCode(AutocareAPIMetadata, models.Model):
    id = models.BigAutoField(primary_key=True)

    pies_code_id = models.IntegerField(
        db_column="PIESCodeId",
        null=True,
        blank=True,
        db_index=True,
    )
    code_value = models.CharField(db_column='CodeValue', max_length=500)
    code_format = models.CharField(db_column='CodeFormat', max_length=500)
    field_format = models.CharField(db_column='FieldFormat', max_length=500, null=True, blank=True)
    code_description = models.CharField(db_column='CodeDescription', max_length=500)
    source = models.CharField(db_column='Source', max_length=500, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = "autocare_pcdb"
        managed = True
        db_table = '"autocare_pcdb"."PIESCode"'
        unique_together = [
            ("pies_code_id", "code_value", "code_format", "source"),
        ]
        indexes = [
            models.Index(fields=["pies_code_id"]),
        ]


