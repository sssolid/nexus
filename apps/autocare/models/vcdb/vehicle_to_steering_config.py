from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class VehicleToSteeringConfig(AutocareAPIMetadata, models.Model):
    vehicle_to_steering_config_id = models.IntegerField(db_column='VehicleToSteeringConfigID', primary_key=True)
    vehicle = models.ForeignKey('Vehicle', db_column='VehicleID', db_index=True, on_delete=models.DO_NOTHING)
    steering_config = models.ForeignKey('SteeringConfig', db_column='SteeringConfigID', db_index=True, on_delete=models.DO_NOTHING)
    source = models.CharField(db_column='Source', max_length=10, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."vehicle_to_steering_config"'
        verbose_name = 'Vehicle To Steering Config'
        verbose_name_plural = 'Vehicle To Steering Configs'
        indexes = [
            models.Index(fields=['vehicle_to_steering_config_id'])
        ]

