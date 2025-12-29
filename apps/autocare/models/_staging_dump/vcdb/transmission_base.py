from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class TransmissionBase(AutocareAPIMetadata, models.Model):
    transmission_base_id = models.IntegerField(db_column='TransmissionBaseID', primary_key=True)
    transmission_type = models.ForeignKey('autocare_vcdb.TransmissionType', db_column='TransmissionTypeID', db_index=True, on_delete=models.DO_NOTHING)
    transmission_num_speeds = models.ForeignKey('autocare_vcdb.TransmissionNumSpeeds', db_column='TransmissionNumSpeedsID', db_index=True, on_delete=models.DO_NOTHING)
    transmission_control_type = models.ForeignKey('autocare_vcdb.TransmissionControlType', db_column='TransmissionControlTypeID', db_index=True, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."TransmissionBase"'
        verbose_name = 'TransmissionBase'
        verbose_name_plural = 'TransmissionBases'
        indexes = [
            models.Index(fields=['transmission_base_id']),
        ]

