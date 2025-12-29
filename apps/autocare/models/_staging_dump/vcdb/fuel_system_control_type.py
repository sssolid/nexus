from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class FuelSystemControlType(AutocareAPIMetadata, models.Model):
    fuel_system_control_type_id = models.IntegerField(db_column='FuelSystemControlTypeID', primary_key=True)
    fuel_system_control_type_name = models.CharField(db_column='FuelSystemControlTypeName', max_length=50)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."FuelSystemControlType"'
        verbose_name = 'FuelSystemControlType'
        verbose_name_plural = 'FuelSystemControlTypes'
        indexes = [
            models.Index(fields=['fuel_system_control_type_id']),
        ]

