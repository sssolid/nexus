from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class VehicleToEngineConfig(AutocareAPIMetadata, models.Model):
    vehicle_to_engine_config_id = models.IntegerField(db_column='VehicleToEngineConfigID', primary_key=True)
    vehicle = models.ForeignKey('autocare_vcdb.Vehicle', db_column='VehicleID', db_index=True, on_delete=models.DO_NOTHING)
    engine_config2 = models.ForeignKey('autocare_vcdb.EngineConfig2', db_column='EngineConfigID', db_index=True, on_delete=models.DO_NOTHING)
    source = models.CharField(db_column='Source', max_length=10, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."vehicle_to_engine_config"'
        app_label = 'autocare_vcdb'
        verbose_name = 'Vehicle To Engine Config'
        verbose_name_plural = 'Vehicle To Engine Configs'
        indexes = [
            models.Index(fields=['vehicle_to_engine_config_id'])
        ]

