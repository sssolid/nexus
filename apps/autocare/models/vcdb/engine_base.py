from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class EngineBase(AutocareAPIMetadata, models.Model):
    engine_base_id = models.IntegerField(db_column='EngineBaseID', primary_key=True)
    liter = models.CharField(db_column='Liter', max_length=6)
    cc = models.CharField(db_column='CC', max_length=8)
    c_id = models.CharField(db_column='CID', max_length=7)
    cylinders = models.CharField(db_column='Cylinders', max_length=2)
    block_type = models.CharField(db_column='BlockType', max_length=2)
    eng_bore_in = models.CharField(db_column='EngBoreIn', max_length=10)
    eng_bore_metric = models.CharField(db_column='EngBoreMetric', max_length=10)
    eng_stroke_in = models.CharField(db_column='EngStrokeIn', max_length=10)
    eng_stroke_metric = models.CharField(db_column='EngStrokeMetric', max_length=10)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."engine_base"'
        verbose_name = 'Engine Base'
        verbose_name_plural = 'Engine Bases'
        indexes = [
            models.Index(fields=['engine_base_id'])
        ]

