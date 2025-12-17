from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class BrakeSystem(AutocareAPIMetadata, models.Model):
    brake_system_id = models.IntegerField(db_column='BrakeSystemID', primary_key=True)
    brake_system_name = models.CharField(db_column='BrakeSystemName', max_length=30)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."brake_system"'
        verbose_name = 'Brake System'
        verbose_name_plural = 'Brake Systems'
        indexes = [
            models.Index(fields=['brake_system_id'])
        ]

