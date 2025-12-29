from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class BrakeABS(AutocareAPIMetadata, models.Model):
    brake_absid = models.IntegerField(db_column='BrakeABSID', primary_key=True)
    brake_abs_name = models.CharField(db_column='BrakeABSName', max_length=30)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."BrakeABS"'
        verbose_name = 'BrakeABS'
        verbose_name_plural = 'BrakeABSs'
        indexes = [
            models.Index(fields=['brake_absid']),
        ]

