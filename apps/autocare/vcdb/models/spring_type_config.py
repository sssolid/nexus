from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class SpringTypeConfig(AutocareAPIMetadata, models.Model):
    spring_type_config_id = models.IntegerField(db_column='SpringTypeConfigID', primary_key=True)
    front_spring_type = models.ForeignKey('autocare_vcdb.SpringType', db_column='FrontSpringTypeID', db_index=True, on_delete=models.DO_NOTHING)
    rear_spring_type = models.ForeignKey('autocare_vcdb.SpringType', db_column='RearSpringTypeID', related_name='springtypeconfig_rearspringtypeid_set', db_index=True, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."spring_type_config"'
        app_label = 'autocare_vcdb'
        verbose_name = 'Spring Type Config'
        verbose_name_plural = 'Spring Type Configs'
        indexes = [
            models.Index(fields=['spring_type_config_id'])
        ]

