from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class VehicleToBrakeConfig(AutocareAPIMetadata, models.Model):
    vehicle_to_brake_config_id = models.IntegerField(db_column='VehicleToBrakeConfigID', primary_key=True)
    vehicle = models.ForeignKey('autocare_vcdb.Vehicle', db_column='VehicleID', db_index=True, on_delete=models.DO_NOTHING)
    brake_config = models.ForeignKey('autocare_vcdb.BrakeConfig', db_column='BrakeConfigID', db_index=True, on_delete=models.DO_NOTHING)
    source = models.CharField(db_column='Source', max_length=10, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."vehicle_to_brake_config"'
        app_label = 'autocare_vcdb'
        verbose_name = 'Vehicle To Brake Config'
        verbose_name_plural = 'Vehicle To Brake Configs'
        indexes = [
            models.Index(fields=['vehicle_to_brake_config_id'])
        ]

