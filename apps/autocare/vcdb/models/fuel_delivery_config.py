from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class FuelDeliveryConfig(AutocareAPIMetadata, models.Model):
    fuel_delivery_config_id = models.IntegerField(db_column='FuelDeliveryConfigID', primary_key=True)
    fuel_delivery_type = models.ForeignKey('autocare_vcdb.FuelDeliveryType', db_column='FuelDeliveryTypeID', db_index=True, on_delete=models.DO_NOTHING)
    fuel_delivery_sub_type = models.ForeignKey('autocare_vcdb.FuelDeliverySubType', db_column='FuelDeliverySubTypeID', db_index=True, on_delete=models.DO_NOTHING)
    fuel_system_control_type = models.ForeignKey('autocare_vcdb.FuelSystemControlType', db_column='FuelSystemControlTypeID', db_index=True, on_delete=models.DO_NOTHING)
    fuel_system_design = models.ForeignKey('autocare_vcdb.FuelSystemDesign', db_column='FuelSystemDesignID', db_index=True, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."fuel_delivery_config"'
        app_label = 'autocare_vcdb'
        verbose_name = 'Fuel Delivery Config'
        verbose_name_plural = 'Fuel Delivery Configs'
        indexes = [
            models.Index(fields=['fuel_delivery_config_id'])
        ]

