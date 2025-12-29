from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class PartsToAlias(AutocareAPIMetadata, models.Model):
    part_terminology = models.ForeignKey('autocare_pcdb.Parts', db_column='PartTerminologyID', db_index=True, on_delete=models.DO_NOTHING)
    alias = models.ForeignKey('autocare_pcdb.Alias', db_column='AliasID', db_index=True, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_pcdb'
        managed = True
        db_table = '"autocare_pcdb"."PartsToAlias"'
        verbose_name = 'PartsToAlias'
        verbose_name_plural = 'PartsToAliass'
        indexes = [
            models.Index(fields=['part_terminology', 'alias']),
        ]

