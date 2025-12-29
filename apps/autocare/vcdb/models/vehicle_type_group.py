from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class VehicleTypeGroup(AutocareAPIMetadata, models.Model):
    vehicle_type_group_id = models.IntegerField(db_column='VehicleTypeGroupID')
    vehicle_type_group_name = models.CharField(db_column='VehicleTypeGroupName', max_length=50)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."vehicle_type_group"'
        app_label = 'autocare_vcdb'
        verbose_name = 'Vehicle Type Group'
        verbose_name_plural = 'Vehicle Type Groups'

