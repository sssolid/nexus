from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class PartsToUse(AutocareAPIMetadata, models.Model):
    part_terminology = models.ForeignKey('autocare_pcdb.Parts', db_column='PartTerminologyID', db_index=True, on_delete=models.DO_NOTHING)
    use = models.ForeignKey('autocare_pcdb.Use', db_column='UseID', db_index=True, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_pcdb'
        managed = True
        db_table = '"autocare_pcdb"."PartsToUse"'
        verbose_name = 'PartsToUse'
        verbose_name_plural = 'PartsToUses'
        indexes = [
            models.Index(fields=['part_terminology', 'use']),
        ]

