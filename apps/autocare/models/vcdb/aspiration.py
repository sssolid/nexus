from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class Aspiration(AutocareAPIMetadata, models.Model):
    aspiration_id = models.IntegerField(db_column='AspirationID', primary_key=True)
    aspiration_name = models.CharField(db_column='AspirationName', max_length=30)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."aspiration"'
        verbose_name = 'Aspiration'
        verbose_name_plural = 'Aspirations'
        indexes = [
            models.Index(fields=['aspiration_id'])
        ]

