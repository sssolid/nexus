from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class VehicleToMfrBodyCode(AutocareAPIMetadata, models.Model):
    vehicle_to_mfr_body_code_id = models.IntegerField(db_column='VehicleToMfrBodyCodeID', primary_key=True)
    vehicle = models.ForeignKey('autocare_vcdb.Vehicle', db_column='VehicleID', db_index=True, on_delete=models.DO_NOTHING)
    mfr_body_code = models.ForeignKey('autocare_vcdb.MfrBodyCode', db_column='MfrBodyCodeID', db_index=True, on_delete=models.DO_NOTHING)
    source = models.CharField(db_column='Source', max_length=10, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."VehicleToMfrBodyCode"'
        verbose_name = 'VehicleToMfrBodyCode'
        verbose_name_plural = 'VehicleToMfrBodyCodes'
        indexes = [
            models.Index(fields=['vehicle_to_mfr_body_code_id']),
        ]

