from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class VehicleToDriveType(AutocareAPIMetadata, models.Model):
    vehicle_to_drive_type_id = models.IntegerField(db_column='VehicleToDriveTypeID', primary_key=True)
    vehicle = models.ForeignKey('autocare_vcdb.Vehicle', db_column='VehicleID', db_index=True, on_delete=models.DO_NOTHING)
    drive_type = models.ForeignKey('autocare_vcdb.DriveType', db_column='DriveTypeID', db_index=True, on_delete=models.DO_NOTHING)
    source = models.CharField(db_column='Source', max_length=10, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."VehicleToDriveType"'
        verbose_name = 'VehicleToDriveType'
        verbose_name_plural = 'VehicleToDriveTypes'
        indexes = [
            models.Index(fields=['vehicle_to_drive_type_id']),
        ]

