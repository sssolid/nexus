from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class BedConfig(AutocareAPIMetadata, models.Model):
    bed_config_id = models.IntegerField(db_column='BedConfigID', primary_key=True)
    bed_length = models.ForeignKey('autocare_vcdb.BedLength', db_column='BedLengthID', db_index=True, on_delete=models.DO_NOTHING)
    bed_type = models.ForeignKey('autocare_vcdb.BedType', db_column='BedTypeID', db_index=True, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."BedConfig"'
        verbose_name = 'BedConfig'
        verbose_name_plural = 'BedConfigs'
        indexes = [
            models.Index(fields=['bed_config_id']),
        ]

