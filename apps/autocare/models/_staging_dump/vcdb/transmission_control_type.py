from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class TransmissionControlType(AutocareAPIMetadata, models.Model):
    transmission_control_type_id = models.IntegerField(db_column='TransmissionControlTypeID', primary_key=True)
    transmission_control_type_name = models.CharField(db_column='TransmissionControlTypeName', max_length=30)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."TransmissionControlType"'
        verbose_name = 'TransmissionControlType'
        verbose_name_plural = 'TransmissionControlTypes'
        indexes = [
            models.Index(fields=['transmission_control_type_id']),
        ]

