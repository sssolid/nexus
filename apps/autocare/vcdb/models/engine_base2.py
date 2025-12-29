from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class EngineBase2(AutocareAPIMetadata, models.Model):
    engine_base_id = models.IntegerField(db_column='EngineBaseID', primary_key=True)
    engine_block = models.ForeignKey('autocare_vcdb.EngineBlock', db_column='EngineBlockID', db_index=True, on_delete=models.DO_NOTHING)
    engine_bore_stroke = models.ForeignKey('autocare_vcdb.EngineBoreStroke', db_column='EngineBoreStrokeID', db_index=True, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."engine_base2"'
        app_label = 'autocare_vcdb'
        verbose_name = 'Engine Base2'
        verbose_name_plural = 'Engine Base2s'
        indexes = [
            models.Index(fields=['engine_base_id'])
        ]

