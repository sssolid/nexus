from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class VehicleToSpringTypeConfig(AutocareAPIMetadata, models.Model):
    vehicle_to_spring_type_config_id = models.IntegerField(db_column='VehicleToSpringTypeConfigID', primary_key=True)
    vehicle = models.ForeignKey('autocare_vcdb.Vehicle', db_column='VehicleID', db_index=True, on_delete=models.DO_NOTHING)
    spring_type_config = models.ForeignKey('autocare_vcdb.SpringTypeConfig', db_column='SpringTypeConfigID', db_index=True, on_delete=models.DO_NOTHING)
    source = models.CharField(db_column='Source', max_length=10, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."vehicle_to_spring_type_config"'
        app_label = 'autocare_vcdb'
        verbose_name = 'Vehicle To Spring Type Config'
        verbose_name_plural = 'Vehicle To Spring Type Configs'
        indexes = [
            models.Index(fields=['vehicle_to_spring_type_config_id'])
        ]

