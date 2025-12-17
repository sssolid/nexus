from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class VehicleToDriveType(AutocareAPIMetadata, models.Model):
    vehicle_to_drive_type_id = models.IntegerField(db_column='VehicleToDriveTypeID', primary_key=True)
    vehicle = models.ForeignKey('Vehicle', db_column='VehicleID', db_index=True, on_delete=models.DO_NOTHING)
    drive_type = models.ForeignKey('DriveType', db_column='DriveTypeID', db_index=True, on_delete=models.DO_NOTHING)
    source = models.CharField(db_column='Source', max_length=10, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."vehicle_to_drive_type"'
        verbose_name = 'Vehicle To Drive Type'
        verbose_name_plural = 'Vehicle To Drive Types'
        indexes = [
            models.Index(fields=['vehicle_to_drive_type_id'])
        ]

