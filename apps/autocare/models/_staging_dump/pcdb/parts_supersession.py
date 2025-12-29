from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class PartsSupersession(AutocareAPIMetadata, models.Model):
    old_part_terminology_id = models.IntegerField(db_column='OldPartTerminologyID', primary_key=True)
    old_part_terminology_name = models.CharField(db_column='OldPartTerminologyName', max_length=200)
    new_part_terminology_id = models.IntegerField(db_column='NewPartTerminologyID', primary_key=True)
    new_part_terminology_name = models.CharField(db_column='NewPartTerminologyName', max_length=200)
    rev_date = models.DateField(db_column='RevDate', null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_pcdb'
        managed = True
        db_table = '"autocare_pcdb"."PartsSupersession"'
        verbose_name = 'PartsSupersession'
        verbose_name_plural = 'PartsSupersessions'
        indexes = [
            models.Index(fields=['old_part_terminology_id', 'new_part_terminology_id']),
        ]

