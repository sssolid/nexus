from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class IgnitionSystemType(AutocareAPIMetadata, models.Model):
    ignition_system_type_id = models.IntegerField(db_column='IgnitionSystemTypeID', primary_key=True)
    ignition_system_type_name = models.CharField(db_column='IgnitionSystemTypeName', max_length=30)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."ignition_system_type"'
        app_label = 'autocare_vcdb'
        verbose_name = 'Ignition System Type'
        verbose_name_plural = 'Ignition System Types'
        indexes = [
            models.Index(fields=['ignition_system_type_id'])
        ]

