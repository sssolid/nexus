from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class EngineDesignation(AutocareAPIMetadata, models.Model):
    engine_designation_id = models.IntegerField(db_column='EngineDesignationID', primary_key=True)
    engine_designation_name = models.CharField(db_column='EngineDesignationName', max_length=30)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."engine_designation"'
        app_label = 'autocare_vcdb'
        verbose_name = 'Engine Designation'
        verbose_name_plural = 'Engine Designations'
        indexes = [
            models.Index(fields=['engine_designation_id'])
        ]

