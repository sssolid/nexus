from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class ValidValues(AutocareAPIMetadata, models.Model):
    valid_value_id = models.IntegerField(db_column='ValidValueID', primary_key=True)
    valid_value = models.CharField(db_column='ValidValue', max_length=100)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_padb'
        managed = True
        db_table = '"autocare_padb"."ValidValues"'
        verbose_name = 'ValidValues'
        verbose_name_plural = 'ValidValuess'
        indexes = [
            models.Index(fields=['valid_value_id']),
        ]

