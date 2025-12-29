from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class WheelBase(AutocareAPIMetadata, models.Model):
    wheel_base_id = models.IntegerField(db_column='WheelBaseID', primary_key=True)
    wheel_base = models.CharField(db_column='WheelBase', max_length=10)
    wheel_base_metric = models.CharField(db_column='WheelBaseMetric', max_length=10)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."WheelBase"'
        verbose_name = 'WheelBase'
        verbose_name_plural = 'WheelBases'
        indexes = [
            models.Index(fields=['wheel_base_id']),
        ]

