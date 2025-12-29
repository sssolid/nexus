from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class EngineBoreStroke(AutocareAPIMetadata, models.Model):
    engine_bore_stroke_id = models.IntegerField(db_column='EngineBoreStrokeID', primary_key=True)
    eng_bore_in = models.CharField(db_column='EngBoreIn', max_length=10)
    eng_bore_metric = models.CharField(db_column='EngBoreMetric', max_length=10)
    eng_stroke_in = models.CharField(db_column='EngStrokeIn', max_length=10)
    eng_stroke_metric = models.CharField(db_column='EngStrokeMetric', max_length=10)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."EngineBoreStroke"'
        verbose_name = 'EngineBoreStroke'
        verbose_name_plural = 'EngineBoreStrokes'
        indexes = [
            models.Index(fields=['engine_bore_stroke_id']),
        ]

