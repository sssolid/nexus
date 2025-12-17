from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class EngineVIN(AutocareAPIMetadata, models.Model):
    engine_vin_id = models.IntegerField(db_column='EngineVINID', primary_key=True)
    engine_vin_name = models.CharField(db_column='EngineVINName', max_length=5)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."engine_vin"'
        verbose_name = 'Engine Vin'
        verbose_name_plural = 'Engine Vins'
        indexes = [
            models.Index(fields=['engine_vin_id'])
        ]

