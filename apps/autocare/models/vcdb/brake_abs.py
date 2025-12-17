from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class BrakeABS(AutocareAPIMetadata, models.Model):
    brake_abs_id = models.IntegerField(db_column='BrakeABSID', primary_key=True)
    brake_abs_name = models.CharField(db_column='BrakeABSName', max_length=30)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."brake_abs"'
        verbose_name = 'Brake Abs'
        verbose_name_plural = 'Brake Abs'
        indexes = [
            models.Index(fields=['brake_abs_id'])
        ]

