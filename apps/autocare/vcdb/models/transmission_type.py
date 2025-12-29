from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class TransmissionType(AutocareAPIMetadata, models.Model):
    transmission_type_id = models.IntegerField(db_column='TransmissionTypeID', primary_key=True)
    transmission_type_name = models.CharField(db_column='TransmissionTypeName', max_length=30)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."transmission_type"'
        app_label = 'autocare_vcdb'
        verbose_name = 'Transmission Type'
        verbose_name_plural = 'Transmission Types'
        indexes = [
            models.Index(fields=['transmission_type_id'])
        ]

