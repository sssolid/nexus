from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class VehicleToBodyConfig(AutocareAPIMetadata, models.Model):
    vehicle_to_body_config_id = models.IntegerField(db_column='VehicleToBodyConfigID', primary_key=True)
    vehicle = models.ForeignKey('autocare_vcdb.Vehicle', db_column='VehicleID', db_index=True, on_delete=models.DO_NOTHING)
    wheel_base = models.ForeignKey('autocare_vcdb.WheelBase', db_column='WheelBaseID', db_index=True, on_delete=models.DO_NOTHING)
    bed_config = models.ForeignKey('autocare_vcdb.BedConfig', db_column='BedConfigID', db_index=True, on_delete=models.DO_NOTHING)
    body_style_config = models.ForeignKey('autocare_vcdb.BodyStyleConfig', db_column='BodyStyleConfigID', db_index=True, on_delete=models.DO_NOTHING)
    mfr_body_code = models.ForeignKey('autocare_vcdb.MfrBodyCode', db_column='MfrBodyCodeID', db_index=True, on_delete=models.DO_NOTHING)
    source = models.CharField(db_column='Source', max_length=10, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."VehicleToBodyConfig"'
        verbose_name = 'VehicleToBodyConfig'
        verbose_name_plural = 'VehicleToBodyConfigs'
        indexes = [
            models.Index(fields=['vehicle_to_body_config_id']),
        ]

