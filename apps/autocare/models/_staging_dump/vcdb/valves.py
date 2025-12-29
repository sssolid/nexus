from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class Valves(AutocareAPIMetadata, models.Model):
    valves_id = models.IntegerField(db_column='ValvesID', primary_key=True)
    valves_per_engine = models.CharField(db_column='ValvesPerEngine', max_length=3)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."Valves"'
        verbose_name = 'Valves'
        verbose_name_plural = 'Valvess'
        indexes = [
            models.Index(fields=['valves_id']),
        ]

