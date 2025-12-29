from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class BrakeType(AutocareAPIMetadata, models.Model):
    brake_type_id = models.IntegerField(db_column='BrakeTypeID', primary_key=True)
    brake_type_name = models.CharField(db_column='BrakeTypeName', max_length=30)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."BrakeType"'
        verbose_name = 'BrakeType'
        verbose_name_plural = 'BrakeTypes'
        indexes = [
            models.Index(fields=['brake_type_id']),
        ]

