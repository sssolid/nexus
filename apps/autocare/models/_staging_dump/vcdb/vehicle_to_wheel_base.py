from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class VehicleToWheelBase(AutocareAPIMetadata, models.Model):
    vehicle_to_wheel_base_id = models.IntegerField(db_column='VehicleToWheelBaseID', primary_key=True)
    vehicle = models.ForeignKey('autocare_vcdb.Vehicle', db_column='VehicleID', db_index=True, on_delete=models.DO_NOTHING)
    wheel_base_id = models.IntegerField(db_column='WheelBaseID')
    source = models.CharField(db_column='Source', max_length=10, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."VehicleToWheelBase"'
        verbose_name = 'VehicleToWheelBase'
        verbose_name_plural = 'VehicleToWheelBases'
        indexes = [
            models.Index(fields=['vehicle_to_wheel_base_id']),
        ]

