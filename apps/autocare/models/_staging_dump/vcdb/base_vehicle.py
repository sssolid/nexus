from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class BaseVehicle(AutocareAPIMetadata, models.Model):
    base_vehicle_id = models.IntegerField(db_column='BaseVehicleID', primary_key=True)
    year = models.ForeignKey('autocare_vcdb.Year', db_column='YearID', db_index=True, on_delete=models.DO_NOTHING)
    make = models.ForeignKey('autocare_vcdb.Make', db_column='MakeID', db_index=True, on_delete=models.DO_NOTHING)
    model = models.ForeignKey('autocare_vcdb.Model', db_column='ModelID', db_index=True, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."BaseVehicle"'
        verbose_name = 'BaseVehicle'
        verbose_name_plural = 'BaseVehicles'
        indexes = [
            models.Index(fields=['base_vehicle_id']),
        ]

