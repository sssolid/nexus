from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class MeasurementGroup(AutocareAPIMetadata, models.Model):
    measurement_group_id = models.IntegerField(db_column='MeasurementGroupID', primary_key=True)
    measurement_group_name = models.CharField(db_column='MeasurementGroupName', max_length=80, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_padb'
        managed = True
        db_table = '"autocare_padb"."MeasurementGroup"'
        verbose_name = 'MeasurementGroup'
        verbose_name_plural = 'MeasurementGroups'
        indexes = [
            models.Index(fields=['measurement_group_id']),
        ]

