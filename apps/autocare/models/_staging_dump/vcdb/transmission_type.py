from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class TransmissionType(AutocareAPIMetadata, models.Model):
    transmission_type_id = models.IntegerField(db_column='TransmissionTypeID', primary_key=True)
    transmission_type_name = models.CharField(db_column='TransmissionTypeName', max_length=30)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."TransmissionType"'
        verbose_name = 'TransmissionType'
        verbose_name_plural = 'TransmissionTypes'
        indexes = [
            models.Index(fields=['transmission_type_id']),
        ]

