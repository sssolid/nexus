from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class Model(AutocareAPIMetadata, models.Model):
    model_id = models.IntegerField(db_column='ModelID', primary_key=True)
    model_name = models.CharField(db_column='ModelName', max_length=100, null=True, blank=True)
    vehicle_type = models.ForeignKey('autocare_vcdb.VehicleType', db_column='VehicleTypeID', db_index=True, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."Model"'
        verbose_name = 'Model'
        verbose_name_plural = 'Models'
        indexes = [
            models.Index(fields=['model_id']),
        ]

