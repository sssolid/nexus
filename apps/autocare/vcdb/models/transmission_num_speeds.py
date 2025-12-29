from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class TransmissionNumSpeeds(AutocareAPIMetadata, models.Model):
    transmission_num_speeds_id = models.IntegerField(db_column='TransmissionNumSpeedsID', primary_key=True)
    transmission_num_speeds = models.CharField(db_column='TransmissionNumSpeeds', max_length=3)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."transmission_num_speeds"'
        app_label = 'autocare_vcdb'
        verbose_name = 'Transmission Num Speeds'
        verbose_name_plural = 'Transmission Num Speeds'
        indexes = [
            models.Index(fields=['transmission_num_speeds_id'])
        ]

