from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class SteeringConfig(AutocareAPIMetadata, models.Model):
    steering_config_id = models.IntegerField(db_column='SteeringConfigID', primary_key=True)
    steering_type = models.ForeignKey('autocare_vcdb.SteeringType', db_column='SteeringTypeID', db_index=True, on_delete=models.DO_NOTHING)
    steering_system = models.ForeignKey('autocare_vcdb.SteeringSystem', db_column='SteeringSystemID', db_index=True, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."steering_config"'
        app_label = 'autocare_vcdb'
        verbose_name = 'Steering Config'
        verbose_name_plural = 'Steering Configs'
        indexes = [
            models.Index(fields=['steering_config_id'])
        ]

