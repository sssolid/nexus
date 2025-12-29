from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class PartsDescription(AutocareAPIMetadata, models.Model):
    parts_description_id = models.IntegerField(db_column='PartsDescriptionID', primary_key=True)
    parts_description = models.CharField(db_column='PartsDescription', max_length=1000)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_pcdb'
        managed = True
        db_table = '"autocare_pcdb"."PartsDescription"'
        verbose_name = 'PartsDescription'
        verbose_name_plural = 'PartsDescriptions'
        indexes = [
            models.Index(fields=['parts_description_id']),
        ]

