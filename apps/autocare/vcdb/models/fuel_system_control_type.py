from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class FuelSystemControlType(AutocareAPIMetadata, models.Model):
    fuel_system_control_type_id = models.IntegerField(db_column='FuelSystemControlTypeID', primary_key=True)
    fuel_system_control_type_name = models.CharField(db_column='FuelSystemControlTypeName', max_length=50)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."fuel_system_control_type"'
        app_label = 'autocare_vcdb'
        verbose_name = 'Fuel System Control Type'
        verbose_name_plural = 'Fuel System Control Types'
        indexes = [
            models.Index(fields=['fuel_system_control_type_id'])
        ]

