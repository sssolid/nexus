from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class BodyStyleConfig(AutocareAPIMetadata, models.Model):
    body_style_config_id = models.IntegerField(db_column='BodyStyleConfigID', primary_key=True)
    body_num_doors = models.ForeignKey('BodyNumDoors', db_column='BodyNumDoorsID', db_index=True, on_delete=models.DO_NOTHING)
    body_type = models.ForeignKey('BodyType', db_column='BodyTypeID', db_index=True, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."body_style_config"'
        verbose_name = 'Body Style Config'
        verbose_name_plural = 'Body Style Configs'
        indexes = [
            models.Index(fields=['body_style_config_id'])
        ]

