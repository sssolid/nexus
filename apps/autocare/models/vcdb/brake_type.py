from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class BrakeType(AutocareAPIMetadata, models.Model):
    brake_type_id = models.IntegerField(db_column='BrakeTypeID', primary_key=True)
    brake_type_name = models.CharField(db_column='BrakeTypeName', max_length=30)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."brake_type"'
        verbose_name = 'Brake Type'
        verbose_name_plural = 'Brake Types'
        indexes = [
            models.Index(fields=['brake_type_id'])
        ]

