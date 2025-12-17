from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class Abbreviation(AutocareAPIMetadata, models.Model):
    abbreviation = models.CharField(db_column='Abbreviation', primary_key=True, max_length=3)
    description = models.CharField(db_column='Description', max_length=20)
    long_description = models.CharField(db_column='LongDescription', max_length=200)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."abbreviation"'
        verbose_name = 'Abbreviation'
        verbose_name_plural = 'Abbreviations'
        indexes = [
            models.Index(fields=['abbreviation'])
        ]

