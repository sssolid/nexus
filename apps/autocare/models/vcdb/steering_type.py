from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class SteeringType(AutocareAPIMetadata, models.Model):
    steering_type_id = models.IntegerField(db_column='SteeringTypeID', primary_key=True)
    steering_type_name = models.CharField(db_column='SteeringTypeName', max_length=30)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."steering_type"'
        verbose_name = 'Steering Type'
        verbose_name_plural = 'Steering Types'
        indexes = [
            models.Index(fields=['steering_type_id'])
        ]

