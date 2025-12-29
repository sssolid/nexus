from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class FuelSystemDesign(AutocareAPIMetadata, models.Model):
    fuel_system_design_id = models.IntegerField(db_column='FuelSystemDesignID', primary_key=True)
    fuel_system_design_name = models.CharField(db_column='FuelSystemDesignName', max_length=50)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."FuelSystemDesign"'
        verbose_name = 'FuelSystemDesign'
        verbose_name_plural = 'FuelSystemDesigns'
        indexes = [
            models.Index(fields=['fuel_system_design_id']),
        ]

