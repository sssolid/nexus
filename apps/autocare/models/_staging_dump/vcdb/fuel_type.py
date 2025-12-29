from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class FuelType(AutocareAPIMetadata, models.Model):
    fuel_type_id = models.IntegerField(db_column='FuelTypeID', primary_key=True)
    fuel_type_name = models.CharField(db_column='FuelTypeName', max_length=30)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."FuelType"'
        verbose_name = 'FuelType'
        verbose_name_plural = 'FuelTypes'
        indexes = [
            models.Index(fields=['fuel_type_id']),
        ]

