from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class BedLength(AutocareAPIMetadata, models.Model):
    bed_length_id = models.IntegerField(db_column='BedLengthID', primary_key=True)
    bed_length = models.CharField(db_column='BedLength', max_length=10)
    bed_length_metric = models.CharField(db_column='BedLengthMetric', max_length=10)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."bed_length"'
        app_label = 'autocare_vcdb'
        verbose_name = 'Bed Length'
        verbose_name_plural = 'Bed Lengths'
        indexes = [
            models.Index(fields=['bed_length_id'])
        ]

