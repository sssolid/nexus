from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class Transmission(AutocareAPIMetadata, models.Model):
    transmission_id = models.IntegerField(db_column='TransmissionID', primary_key=True)
    transmission_base = models.ForeignKey('TransmissionBase', db_column='TransmissionBaseID', db_index=True, on_delete=models.DO_NOTHING)
    transmission_mfr_code = models.ForeignKey('TransmissionMfrCode', db_column='TransmissionMfrCodeID', db_index=True, on_delete=models.DO_NOTHING)
    elec_controlled = models.ForeignKey('ElecControlled', db_column='TransmissionElecControlledID', db_index=True, on_delete=models.DO_NOTHING)
    mfr = models.ForeignKey('Mfr', db_column='TransmissionMfrID', db_index=True, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."transmission"'
        verbose_name = 'Transmission'
        verbose_name_plural = 'Transmissions'
        indexes = [
            models.Index(fields=['transmission_id'])
        ]

