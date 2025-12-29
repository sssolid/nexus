from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class VehicleType(AutocareAPIMetadata, models.Model):
    vehicle_type_id = models.IntegerField(db_column='VehicleTypeID', primary_key=True)
    vehicle_type_name = models.CharField(db_column='VehicleTypeName', max_length=50)
    vehicle_type_group_id = models.IntegerField(db_column='VehicleTypeGroupID', blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."vehicle_type"'
        app_label = 'autocare_vcdb'
        verbose_name = 'Vehicle Type'
        verbose_name_plural = 'Vehicle Types'
        indexes = [
            models.Index(fields=['vehicle_type_id'])
        ]

