from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class ElecControlled(AutocareAPIMetadata, models.Model):
    elec_controlled_id = models.IntegerField(db_column='ElecControlledID', primary_key=True)
    elec_controlled = models.CharField(db_column='ElecControlled', max_length=3)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."ElecControlled"'
        verbose_name = 'ElecControlled'
        verbose_name_plural = 'ElecControlleds'
        indexes = [
            models.Index(fields=['elec_controlled_id']),
        ]

