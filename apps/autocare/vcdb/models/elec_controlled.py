from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class ElecControlled(AutocareAPIMetadata, models.Model):
    elec_controlled_id = models.IntegerField(db_column='ElecControlledID', primary_key=True)
    elec_controlled = models.CharField(db_column='ElecControlled', max_length=3)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."elec_controlled"'
        app_label = 'autocare_vcdb'
        verbose_name = 'Elec Controlled'
        verbose_name_plural = 'Elec Controlleds'
        indexes = [
            models.Index(fields=['elec_controlled_id'])
        ]

