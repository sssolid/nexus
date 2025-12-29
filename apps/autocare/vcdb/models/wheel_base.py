from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class WheelBase(AutocareAPIMetadata, models.Model):
    wheel_base_id = models.IntegerField(db_column='WheelBaseID', primary_key=True)
    wheel_base = models.CharField(db_column='WheelBase', max_length=10)
    wheel_base_metric = models.CharField(db_column='WheelBaseMetric', max_length=10)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."wheel_base"'
        app_label = 'autocare_vcdb'
        verbose_name = 'Wheel Base'
        verbose_name_plural = 'Wheel Bases'
        indexes = [
            models.Index(fields=['wheel_base_id'])
        ]

