from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class DriveType(AutocareAPIMetadata, models.Model):
    drive_type_id = models.IntegerField(db_column='DriveTypeID', primary_key=True)
    drive_type_name = models.CharField(db_column='DriveTypeName', max_length=30)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."drive_type"'
        verbose_name = 'Drive Type'
        verbose_name_plural = 'Drive Types'
        indexes = [
            models.Index(fields=['drive_type_id'])
        ]

