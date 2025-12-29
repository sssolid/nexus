from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class SteeringSystem(AutocareAPIMetadata, models.Model):
    steering_system_id = models.IntegerField(db_column='SteeringSystemID', primary_key=True)
    steering_system_name = models.CharField(db_column='SteeringSystemName', max_length=30)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."steering_system"'
        app_label = 'autocare_vcdb'
        verbose_name = 'Steering System'
        verbose_name_plural = 'Steering Systems'
        indexes = [
            models.Index(fields=['steering_system_id'])
        ]

