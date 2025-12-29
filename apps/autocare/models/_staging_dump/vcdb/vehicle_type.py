from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class VehicleType(AutocareAPIMetadata, models.Model):
    vehicle_type_id = models.IntegerField(db_column='VehicleTypeID', primary_key=True)
    vehicle_type_name = models.CharField(db_column='VehicleTypeName', max_length=50)
    vehicle_type_group_id = models.IntegerField(db_column='VehicleTypeGroupID', null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."VehicleType"'
        verbose_name = 'VehicleType'
        verbose_name_plural = 'VehicleTypes'
        indexes = [
            models.Index(fields=['vehicle_type_id']),
        ]

