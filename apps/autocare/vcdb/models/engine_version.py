from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class EngineVersion(AutocareAPIMetadata, models.Model):
    engine_version_id = models.IntegerField(db_column='EngineVersionID', primary_key=True)
    engine_version = models.CharField(db_column='EngineVersion', max_length=20)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."engine_version"'
        app_label = 'autocare_vcdb'
        verbose_name = 'Engine Version'
        verbose_name_plural = 'Engine Versions'
        indexes = [
            models.Index(fields=['engine_version_id'])
        ]

