from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class VehicleToSteeringConfig(AutocareAPIMetadata, models.Model):
    vehicle_to_steering_config_id = models.IntegerField(db_column='VehicleToSteeringConfigID', primary_key=True)
    vehicle = models.ForeignKey('autocare_vcdb.Vehicle', db_column='VehicleID', db_index=True, on_delete=models.DO_NOTHING)
    steering_config = models.ForeignKey('autocare_vcdb.SteeringConfig', db_column='SteeringConfigID', db_index=True, on_delete=models.DO_NOTHING)
    source = models.CharField(db_column='Source', max_length=10, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."VehicleToSteeringConfig"'
        verbose_name = 'VehicleToSteeringConfig'
        verbose_name_plural = 'VehicleToSteeringConfigs'
        indexes = [
            models.Index(fields=['vehicle_to_steering_config_id']),
        ]

