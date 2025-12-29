from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class FuelDeliverySubType(AutocareAPIMetadata, models.Model):
    fuel_delivery_sub_type_id = models.IntegerField(db_column='FuelDeliverySubTypeID', primary_key=True)
    fuel_delivery_sub_type_name = models.CharField(db_column='FuelDeliverySubTypeName', max_length=50)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."FuelDeliverySubType"'
        verbose_name = 'FuelDeliverySubType'
        verbose_name_plural = 'FuelDeliverySubTypes'
        indexes = [
            models.Index(fields=['fuel_delivery_sub_type_id']),
        ]

