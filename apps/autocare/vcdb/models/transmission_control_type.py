from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class TransmissionControlType(AutocareAPIMetadata, models.Model):
    transmission_control_type_id = models.IntegerField(db_column='TransmissionControlTypeID', primary_key=True)
    transmission_control_type_name = models.CharField(db_column='TransmissionControlTypeName', max_length=30)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."transmission_control_type"'
        app_label = 'autocare_vcdb'
        verbose_name = 'Transmission Control Type'
        verbose_name_plural = 'Transmission Control Types'
        indexes = [
            models.Index(fields=['transmission_control_type_id'])
        ]

