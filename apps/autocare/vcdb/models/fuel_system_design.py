from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class FuelSystemDesign(AutocareAPIMetadata, models.Model):
    fuel_system_design_id = models.IntegerField(db_column='FuelSystemDesignID', primary_key=True)
    fuel_system_design_name = models.CharField(db_column='FuelSystemDesignName', max_length=50)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."fuel_system_design"'
        app_label = 'autocare_vcdb'
        verbose_name = 'Fuel System Design'
        verbose_name_plural = 'Fuel System Designs'
        indexes = [
            models.Index(fields=['fuel_system_design_id'])
        ]

