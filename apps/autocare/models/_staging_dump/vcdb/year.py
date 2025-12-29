from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class Year(AutocareAPIMetadata, models.Model):
    year_id = models.IntegerField(db_column='YearID', primary_key=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."Year"'
        verbose_name = 'Year'
        verbose_name_plural = 'Years'
        indexes = [
            models.Index(fields=['year_id']),
        ]

