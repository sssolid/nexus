from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class VehicleToClass(AutocareAPIMetadata, models.Model):
    vehicle_to_class_id = models.IntegerField(
        db_column="VehicleToClassID",
        primary_key=True,
    )

    vehicle = models.ForeignKey(
        "autocare_vcdb.Vehicle",
        db_column="VehicleID",
        db_index=True,
        on_delete=models.DO_NOTHING,
        related_name="vehicle_classes",
    )

    vehicle_class = models.ForeignKey(
        "autocare_vcdb.VehicleClass",
        db_column="ClassID",
        db_index=True,
        on_delete=models.DO_NOTHING,
        related_name="vehicles",
    )

    source = models.CharField(
        db_column="Source",
        max_length=10,
        blank=True,
        null=True,
    )

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."vehicle_to_class"'
        app_label = 'autocare_vcdb'
        verbose_name = "Vehicle To Classv Class"
        verbose_name_plural = "Vehicle To Class"


