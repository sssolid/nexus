from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class VehicleToEngineConfig(AutocareAPIMetadata, models.Model):
    vehicle_to_engine_config_id = models.IntegerField(db_column='VehicleToEngineConfigID', primary_key=True)
    vehicle = models.ForeignKey('autocare_vcdb.Vehicle', db_column='VehicleID', db_index=True, on_delete=models.DO_NOTHING)
    engine_config = models.ForeignKey('autocare_vcdb.EngineConfig2', db_column='EngineConfigID', db_index=True, on_delete=models.DO_NOTHING)
    source = models.CharField(db_column='Source', max_length=10, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."VehicleToEngineConfig"'
        verbose_name = 'VehicleToEngineConfig'
        verbose_name_plural = 'VehicleToEngineConfigs'
        indexes = [
            models.Index(fields=['vehicle_to_engine_config_id']),
        ]

