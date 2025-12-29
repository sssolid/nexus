from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class BodyStyleConfig(AutocareAPIMetadata, models.Model):
    body_style_config_id = models.IntegerField(db_column='BodyStyleConfigID', primary_key=True)
    body_num_doors = models.ForeignKey('autocare_vcdb.BodyNumDoors', db_column='BodyNumDoorsID', db_index=True, on_delete=models.DO_NOTHING)
    body_type = models.ForeignKey('autocare_vcdb.BodyType', db_column='BodyTypeID', db_index=True, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."BodyStyleConfig"'
        verbose_name = 'BodyStyleConfig'
        verbose_name_plural = 'BodyStyleConfigs'
        indexes = [
            models.Index(fields=['body_style_config_id']),
        ]

