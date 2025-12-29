from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class EngineVersion(AutocareAPIMetadata, models.Model):
    engine_version_id = models.IntegerField(db_column='EngineVersionID', primary_key=True)
    engine_version = models.CharField(db_column='EngineVersion', max_length=20)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."EngineVersion"'
        verbose_name = 'EngineVersion'
        verbose_name_plural = 'EngineVersions'
        indexes = [
            models.Index(fields=['engine_version_id']),
        ]

