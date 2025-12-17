from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class VehicleToClass(AutocareAPIMetadata, models.Model):
    vehicle_to_class_id = models.IntegerField(db_column='VehicleToClassID', primary_key=True)
    vehicle = models.ForeignKey('Vehicle', db_column='VehicleID', db_index=True, on_delete=models.DO_NOTHING)
    vehicle_class = models.ForeignKey('VehicleClass', db_column='ClassID', db_index=True, on_delete=models.DO_NOTHING)
    source = models.CharField(db_column='Source', max_length=10, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."vehicle_to_class"'
        verbose_name = 'Vehicle To Class'
        verbose_name_plural = 'Vehicle To Class'
        indexes = [
            models.Index(fields=['vehicle_to_class_id'])
        ]

