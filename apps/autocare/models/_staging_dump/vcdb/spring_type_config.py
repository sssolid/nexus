from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class SpringTypeConfig(AutocareAPIMetadata, models.Model):
    spring_type_config_id = models.IntegerField(db_column='SpringTypeConfigID', primary_key=True)
    front_spring_type = models.ForeignKey('autocare_vcdb.SpringType', db_column='FrontSpringTypeID', db_index=True, on_delete=models.DO_NOTHING)
    rear_spring_type = models.ForeignKey('autocare_vcdb.SpringType', db_column='RearSpringTypeID', db_index=True, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."SpringTypeConfig"'
        verbose_name = 'SpringTypeConfig'
        verbose_name_plural = 'SpringTypeConfigs'
        indexes = [
            models.Index(fields=['spring_type_config_id']),
        ]

