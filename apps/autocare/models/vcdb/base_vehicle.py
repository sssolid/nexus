from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class BaseVehicle(AutocareAPIMetadata, models.Model):
    base_vehicle_id = models.IntegerField(db_column='BaseVehicleID', primary_key=True)
    vehicle_year = models.ForeignKey('Year', db_column='YearID', db_index=True, on_delete=models.DO_NOTHING)
    make = models.ForeignKey('Make', db_column='MakeID', db_index=True, on_delete=models.DO_NOTHING)
    vehicle_model = models.ForeignKey('VehicleModel', db_column='ModelID', db_index=True, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."base_vehicle"'
        verbose_name = 'Base Vehicle'
        verbose_name_plural = 'Base Vehicles'
        indexes = [
            models.Index(fields=['base_vehicle_id'])
        ]

