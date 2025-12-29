from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class FuelDeliverySubType(AutocareAPIMetadata, models.Model):
    fuel_delivery_sub_type_id = models.IntegerField(db_column='FuelDeliverySubTypeID', primary_key=True)
    fuel_delivery_sub_type_name = models.CharField(db_column='FuelDeliverySubTypeName', max_length=50)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."fuel_delivery_sub_type"'
        app_label = 'autocare_vcdb'
        verbose_name = 'Fuel Delivery Sub Type'
        verbose_name_plural = 'Fuel Delivery Sub Types'
        indexes = [
            models.Index(fields=['fuel_delivery_sub_type_id'])
        ]

