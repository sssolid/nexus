from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class SteeringConfig(AutocareAPIMetadata, models.Model):
    steering_config_id = models.IntegerField(db_column='SteeringConfigID', primary_key=True)
    steering_type = models.ForeignKey('autocare_vcdb.SteeringType', db_column='SteeringTypeID', db_index=True, on_delete=models.DO_NOTHING)
    steering_system = models.ForeignKey('autocare_vcdb.SteeringSystem', db_column='SteeringSystemID', db_index=True, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."SteeringConfig"'
        verbose_name = 'SteeringConfig'
        verbose_name_plural = 'SteeringConfigs'
        indexes = [
            models.Index(fields=['steering_config_id']),
        ]

