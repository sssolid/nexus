from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class EngineConfig2(AutocareAPIMetadata, models.Model):
    engine_config_id = models.IntegerField(db_column='EngineConfigID', primary_key=True)
    engine_designation = models.ForeignKey('EngineDesignation', db_column='EngineDesignationID', db_index=True, on_delete=models.DO_NOTHING)
    engine_vin = models.ForeignKey('EngineVIN', db_column='EngineVINID', db_index=True, on_delete=models.DO_NOTHING)
    valves = models.ForeignKey('Valves', db_column='ValvesID', db_index=True, on_delete=models.DO_NOTHING)
    engine_base2 = models.ForeignKey('EngineBase2', db_column='EngineBaseID', db_index=True, on_delete=models.DO_NOTHING)
    engine_block = models.ForeignKey('EngineBlock', db_column='EngineBlockID', db_index=True, on_delete=models.DO_NOTHING)
    engine_bore_stroke = models.ForeignKey('EngineBoreStroke', db_column='EngineBoreStrokeID', db_index=True, on_delete=models.DO_NOTHING)
    fuel_delivery_config = models.ForeignKey('FuelDeliveryConfig', db_column='FuelDeliveryConfigID', db_index=True, on_delete=models.DO_NOTHING)
    aspiration = models.ForeignKey('Aspiration', db_column='AspirationID', db_index=True, on_delete=models.DO_NOTHING)
    cylinder_head_type = models.ForeignKey('CylinderHeadType', db_column='CylinderHeadTypeID', db_index=True, on_delete=models.DO_NOTHING)
    fuel_type = models.ForeignKey('FuelType', db_column='FuelTypeID', db_index=True, on_delete=models.DO_NOTHING)
    ignition_system_type = models.ForeignKey('IgnitionSystemType', db_column='IgnitionSystemTypeID', db_index=True, on_delete=models.DO_NOTHING)
    mfr = models.ForeignKey('Mfr', db_column='EngineMfrID', db_index=True, on_delete=models.DO_NOTHING)
    engine_version = models.ForeignKey('EngineVersion', db_column='EngineVersionID', db_index=True, on_delete=models.DO_NOTHING)
    power_output_id = models.IntegerField(db_column='PowerOutputID')

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."engine_config2"'
        verbose_name = 'Engine Config2'
        verbose_name_plural = 'Engine Config2s'
        indexes = [
            models.Index(fields=['engine_config_id'])
        ]

