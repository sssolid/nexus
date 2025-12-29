from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class BedLength(AutocareAPIMetadata, models.Model):
    bed_length_id = models.IntegerField(db_column='BedLengthID', primary_key=True)
    bed_length = models.CharField(db_column='BedLength', max_length=10)
    bed_length_metric = models.CharField(db_column='BedLengthMetric', max_length=10)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."BedLength"'
        verbose_name = 'BedLength'
        verbose_name_plural = 'BedLengths'
        indexes = [
            models.Index(fields=['bed_length_id']),
        ]

