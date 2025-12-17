from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class VehicleToWheelBase(AutocareAPIMetadata, models.Model):
    vehicle_to_wheel_base_id = models.IntegerField(db_column='VehicleToWheelBaseID', primary_key=True)
    vehicle = models.ForeignKey('Vehicle', db_column='VehicleID', db_index=True, on_delete=models.DO_NOTHING)
    wheel_base_id = models.IntegerField(db_column='WheelBaseID')
    source = models.CharField(db_column='Source', max_length=10, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."vehicle_to_wheel_base"'
        verbose_name = 'Vehicle To Wheel Base'
        verbose_name_plural = 'Vehicle To Wheel Bases'
        indexes = [
            models.Index(fields=['vehicle_to_wheel_base_id'])
        ]

