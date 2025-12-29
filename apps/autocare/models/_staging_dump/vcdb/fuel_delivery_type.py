from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class FuelDeliveryType(AutocareAPIMetadata, models.Model):
    fuel_delivery_type_id = models.IntegerField(db_column='FuelDeliveryTypeID', primary_key=True)
    fuel_delivery_type_name = models.CharField(db_column='FuelDeliveryTypeName', max_length=50)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."FuelDeliveryType"'
        verbose_name = 'FuelDeliveryType'
        verbose_name_plural = 'FuelDeliveryTypes'
        indexes = [
            models.Index(fields=['fuel_delivery_type_id']),
        ]

