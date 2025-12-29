from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class IgnitionSystemType(AutocareAPIMetadata, models.Model):
    ignition_system_type_id = models.IntegerField(db_column='IgnitionSystemTypeID', primary_key=True)
    ignition_system_type_name = models.CharField(db_column='IgnitionSystemTypeName', max_length=30)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."IgnitionSystemType"'
        verbose_name = 'IgnitionSystemType'
        verbose_name_plural = 'IgnitionSystemTypes'
        indexes = [
            models.Index(fields=['ignition_system_type_id']),
        ]

