from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class VehicleTypeGroup(AutocareAPIMetadata, models.Model):
    vehicle_type_group_id = models.IntegerField(db_column='VehicleTypeGroupID')
    vehicle_type_group_name = models.CharField(db_column='VehicleTypeGroupName', max_length=50)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."VehicleTypeGroup"'
        verbose_name = 'VehicleTypeGroup'
        verbose_name_plural = 'VehicleTypeGroups'
        indexes = []

