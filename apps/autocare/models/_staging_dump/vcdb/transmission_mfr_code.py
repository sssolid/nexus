from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class TransmissionMfrCode(AutocareAPIMetadata, models.Model):
    transmission_mfr_code_id = models.IntegerField(db_column='TransmissionMfrCodeID', primary_key=True)
    transmission_mfr_code = models.CharField(db_column='TransmissionMfrCode', max_length=30)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."TransmissionMfrCode"'
        verbose_name = 'TransmissionMfrCode'
        verbose_name_plural = 'TransmissionMfrCodes'
        indexes = [
            models.Index(fields=['transmission_mfr_code_id']),
        ]

