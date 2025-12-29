from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class PIESReferenceFieldCode(AutocareAPIMetadata, models.Model):
    pies_reference_field_code_id = models.IntegerField(db_column='PIESReferenceFieldCodeId', primary_key=True)
    pies_field = models.ForeignKey('autocare_pcdb.PIESField', db_column='PIESFieldId', db_index=True, on_delete=models.DO_NOTHING)
    pies_code = models.ForeignKey('autocare_pcdb.PIESCode', db_column='PIESCodeId', db_index=True, on_delete=models.DO_NOTHING)
    pies_expi_code = models.ForeignKey('autocare_pcdb.PIESExpiCode', db_column='PIESExpiCodeId', db_index=True, on_delete=models.DO_NOTHING)
    reference_notes = models.CharField(db_column='ReferenceNotes', max_length=2000, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_pcdb'
        managed = True
        db_table = '"autocare_pcdb"."PIESReferenceFieldCode"'
        verbose_name = 'PIESReferenceFieldCode'
        verbose_name_plural = 'PIESReferenceFieldCodes'
        indexes = [
            models.Index(fields=['pies_reference_field_code_id']),
        ]

