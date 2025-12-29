from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class BedType(AutocareAPIMetadata, models.Model):
    bed_type_id = models.IntegerField(db_column='BedTypeID', primary_key=True)
    bed_type_name = models.CharField(db_column='BedTypeName', max_length=50)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."BedType"'
        verbose_name = 'BedType'
        verbose_name_plural = 'BedTypes'
        indexes = [
            models.Index(fields=['bed_type_id']),
        ]

