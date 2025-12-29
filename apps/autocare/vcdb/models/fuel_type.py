from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class FuelType(AutocareAPIMetadata, models.Model):
    fuel_type_id = models.IntegerField(db_column='FuelTypeID', primary_key=True)
    fuel_type_name = models.CharField(db_column='FuelTypeName', max_length=30)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."fuel_type"'
        app_label = 'autocare_vcdb'
        verbose_name = 'Fuel Type'
        verbose_name_plural = 'Fuel Types'
        indexes = [
            models.Index(fields=['fuel_type_id'])
        ]

