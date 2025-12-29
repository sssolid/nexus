from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class EngineVIN(AutocareAPIMetadata, models.Model):
    engine_vinid = models.IntegerField(db_column='EngineVINID', primary_key=True)
    engine_vin_name = models.CharField(db_column='EngineVINName', max_length=5)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."EngineVIN"'
        verbose_name = 'EngineVIN'
        verbose_name_plural = 'EngineVINs'
        indexes = [
            models.Index(fields=['engine_vinid']),
        ]

