from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class PIESField(AutocareAPIMetadata, models.Model):
    pies_field_id = models.IntegerField(db_column='PIESFieldId', primary_key=True)
    field_name = models.CharField(db_column='FieldName', max_length=500)
    reference_field_number = models.CharField(db_column='ReferenceFieldNumber', max_length=500)
    pies_segment = models.ForeignKey('autocare_pcdb.PIESSegment', db_column='PIESSegmentId', db_index=True, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_pcdb'
        managed = True
        db_table = '"autocare_pcdb"."PIESField"'
        verbose_name = 'PIESField'
        verbose_name_plural = 'PIESFields'
        indexes = [
            models.Index(fields=['pies_field_id']),
        ]

