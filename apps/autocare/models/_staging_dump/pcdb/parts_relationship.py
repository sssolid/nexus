from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class PartsRelationship(AutocareAPIMetadata, models.Model):
    part_terminology = models.ForeignKey('autocare_pcdb.Parts', db_column='PartTerminologyID', db_index=True, on_delete=models.DO_NOTHING)
    related_part_terminology = models.ForeignKey('autocare_pcdb.Parts', db_column='RelatedPartTerminologyID', db_index=True, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_pcdb'
        managed = True
        db_table = '"autocare_pcdb"."PartsRelationship"'
        verbose_name = 'PartsRelationship'
        verbose_name_plural = 'PartsRelationships'
        indexes = [
            models.Index(fields=['part_terminology', 'related_part_terminology']),
        ]

