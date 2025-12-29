from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class SteeringType(AutocareAPIMetadata, models.Model):
    steering_type_id = models.IntegerField(db_column='SteeringTypeID', primary_key=True)
    steering_type_name = models.CharField(db_column='SteeringTypeName', max_length=30)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."SteeringType"'
        verbose_name = 'SteeringType'
        verbose_name_plural = 'SteeringTypes'
        indexes = [
            models.Index(fields=['steering_type_id']),
        ]

