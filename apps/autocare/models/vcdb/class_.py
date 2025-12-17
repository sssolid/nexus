from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class VehicleClass(AutocareAPIMetadata, models.Model):
    class_id = models.IntegerField(db_column='ClassID', primary_key=True)
    class_name = models.CharField(db_column='ClassName', max_length=30)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."class"'
        verbose_name = 'Class'
        verbose_name_plural = 'Class'
        indexes = [
            models.Index(fields=['class_id'])
        ]

