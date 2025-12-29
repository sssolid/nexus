from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class PowerOutput(AutocareAPIMetadata, models.Model):
    power_output_id = models.IntegerField(db_column='PowerOutputID')
    horse_power = models.CharField(db_column='HorsePower', max_length=10)
    kilowatt_power = models.CharField(db_column='KilowattPower', max_length=10)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."power_output"'
        app_label = 'autocare_vcdb'
        verbose_name = 'Power Output'
        verbose_name_plural = 'Power Outputs'

