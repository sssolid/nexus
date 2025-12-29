from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class Vehicle(AutocareAPIMetadata, models.Model):
    vehicle_id = models.IntegerField(db_column='VehicleID', primary_key=True)
    base_vehicle = models.ForeignKey('autocare_vcdb.BaseVehicle', db_column='BaseVehicleID', db_index=True, on_delete=models.DO_NOTHING)
    submodel = models.ForeignKey('autocare_vcdb.SubModel', db_column='SubmodelID', db_index=True, on_delete=models.DO_NOTHING)
    region = models.ForeignKey('autocare_vcdb.Region', db_column='RegionID', db_index=True, on_delete=models.DO_NOTHING)
    source = models.CharField(db_column='Source', max_length=10, null=True, blank=True)
    publication_stage = models.ForeignKey('autocare_vcdb.PublicationStage', db_column='PublicationStageID', db_index=True, on_delete=models.DO_NOTHING)
    publication_stage_source = models.CharField(db_column='PublicationStageSource', max_length=100)
    publication_stage_date = models.DateTimeField(db_column='PublicationStageDate')

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."Vehicle"'
        verbose_name = 'Vehicle'
        verbose_name_plural = 'Vehicles'
        indexes = [
            models.Index(fields=['vehicle_id']),
        ]

