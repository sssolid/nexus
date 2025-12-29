from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class VehicleToClass(AutocareAPIMetadata, models.Model):
    vehicle_to_class_id = models.IntegerField(db_column='VehicleToClassID', primary_key=True)
    vehicle = models.ForeignKey('autocare_vcdb.Vehicle', db_column='VehicleID', db_index=True, on_delete=models.DO_NOTHING)
    class_ = models.ForeignKey('autocare_vcdb.Class', db_column='ClassID', db_index=True, on_delete=models.DO_NOTHING)
    source = models.CharField(db_column='Source', max_length=10, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."VehicleToClass"'
        verbose_name = 'VehicleToClass'
        verbose_name_plural = 'VehicleToClasss'
        indexes = [
            models.Index(fields=['vehicle_to_class_id']),
        ]

