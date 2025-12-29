from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class Parts(AutocareAPIMetadata, models.Model):
    part_terminology_id = models.IntegerField(db_column='PartTerminologyID', primary_key=True)
    part_terminology_name = models.CharField(db_column='PartTerminologyName', max_length=500)
    parts_description = models.ForeignKey('autocare_pcdb.PartsDescription', db_column='PartsDescriptionID', db_index=True, on_delete=models.DO_NOTHING)
    rev_date = models.DateField(db_column='RevDate', null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_pcdb'
        managed = True
        db_table = '"autocare_pcdb"."Parts"'
        verbose_name = 'Parts'
        verbose_name_plural = 'Partss'
        indexes = [
            models.Index(fields=['part_terminology_id']),
        ]

