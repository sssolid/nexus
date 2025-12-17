from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class Mfr(AutocareAPIMetadata, models.Model):
    mfr_id = models.IntegerField(db_column='MfrID', primary_key=True)
    mfr_name = models.CharField(db_column='MfrName', max_length=30)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."mfr"'
        verbose_name = 'Mfr'
        verbose_name_plural = 'Mfrs'
        indexes = [
            models.Index(fields=['mfr_id'])
        ]

