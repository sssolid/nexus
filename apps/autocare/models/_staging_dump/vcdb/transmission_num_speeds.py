from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class TransmissionNumSpeeds(AutocareAPIMetadata, models.Model):
    transmission_num_speeds_id = models.IntegerField(db_column='TransmissionNumSpeedsID', primary_key=True)
    transmission_num_speeds = models.TextField(db_column='TransmissionNumSpeeds')

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."TransmissionNumSpeeds"'
        verbose_name = 'TransmissionNumSpeeds'
        verbose_name_plural = 'TransmissionNumSpeedss'
        indexes = [
            models.Index(fields=['transmission_num_speeds_id']),
        ]

