from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class Vehicle(AutocareAPIMetadata, models.Model):
    vehicle_id = models.IntegerField(db_column='VehicleID', primary_key=True)
    base_vehicle = models.ForeignKey('autocare_vcdb.BaseVehicle', db_column='BaseVehicleID', db_index=True, on_delete=models.DO_NOTHING)
    sub_model = models.ForeignKey('autocare_vcdb.SubModel', db_column='SubmodelID', db_index=True, on_delete=models.DO_NOTHING)
    region = models.ForeignKey('autocare_vcdb.Region', db_column='RegionID', db_index=True, on_delete=models.DO_NOTHING)
    source = models.CharField(db_column='Source', max_length=10, blank=True, null=True)
    publication_stage = models.ForeignKey('autocare_vcdb.PublicationStage', db_column='PublicationStageID', db_index=True, blank=True, null=True, on_delete=models.DO_NOTHING)
    publication_stage_source = models.CharField(db_column='PublicationStageSource', max_length=100, blank=True, null=True)
    publication_stage_date = models.DateTimeField(db_column='PublicationStageDate', blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."vehicle"'
        app_label = 'autocare_vcdb'
        verbose_name = 'Vehicle'
        verbose_name_plural = 'Vehicles'
        indexes = [
            models.Index(fields=['vehicle_id'])
        ]

