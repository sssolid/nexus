from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class Alias(AutocareAPIMetadata, models.Model):
    alias_id = models.IntegerField(db_column='AliasID', primary_key=True)
    alias_name = models.CharField(db_column='AliasName', max_length=100)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_pcdb'
        managed = True
        db_table = '"autocare_pcdb"."Alias"'
        verbose_name = 'Alias'
        verbose_name_plural = 'Aliass'
        indexes = [
            models.Index(fields=['alias_id']),
        ]

