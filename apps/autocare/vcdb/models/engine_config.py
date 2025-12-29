from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class EngineConfig(AutocareAPIMetadata, models.Model):
    engine_config_id = models.IntegerField(db_column='EngineConfigID', primary_key=True)
    engine_designation = models.ForeignKey('autocare_vcdb.EngineDesignation', db_column='EngineDesignationID', db_index=True, on_delete=models.DO_NOTHING)
    engine_vin = models.ForeignKey('autocare_vcdb.EngineVIN', db_column='EngineVINID', db_index=True, on_delete=models.DO_NOTHING)
    valves = models.ForeignKey('autocare_vcdb.Valves', db_column='ValvesID', db_index=True, on_delete=models.DO_NOTHING)
    engine_base = models.ForeignKey('autocare_vcdb.EngineBase', db_column='EngineBaseID', db_index=True, on_delete=models.DO_NOTHING)
    fuel_delivery_config = models.ForeignKey('autocare_vcdb.FuelDeliveryConfig', db_column='FuelDeliveryConfigID', db_index=True, on_delete=models.DO_NOTHING)
    aspiration = models.ForeignKey('autocare_vcdb.Aspiration', db_column='AspirationID', db_index=True, on_delete=models.DO_NOTHING)
    cylinder_head_type = models.ForeignKey('autocare_vcdb.CylinderHeadType', db_column='CylinderHeadTypeID', db_index=True, on_delete=models.DO_NOTHING)
    fuel_type = models.ForeignKey('autocare_vcdb.FuelType', db_column='FuelTypeID', db_index=True, on_delete=models.DO_NOTHING)
    ignition_system_type = models.ForeignKey('autocare_vcdb.IgnitionSystemType', db_column='IgnitionSystemTypeID', db_index=True, on_delete=models.DO_NOTHING)
    mfr = models.ForeignKey('autocare_vcdb.Mfr', db_column='EngineMfrID', db_index=True, on_delete=models.DO_NOTHING)
    engine_version = models.ForeignKey('autocare_vcdb.EngineVersion', db_column='EngineVersionID', db_index=True, on_delete=models.DO_NOTHING)
    power_output_id = models.IntegerField(db_column='PowerOutputID')

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."engine_config"'
        app_label = 'autocare_vcdb'
        verbose_name = 'Engine Config'
        verbose_name_plural = 'Engine Configs'
        indexes = [
            models.Index(fields=['engine_config_id'])
        ]

