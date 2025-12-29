from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class PowerOutput(AutocareAPIMetadata, models.Model):
    power_output_id = models.IntegerField(db_column='PowerOutputID')
    horse_power = models.CharField(db_column='HorsePower', max_length=10)
    kilowatt_power = models.CharField(db_column='KilowattPower', max_length=10)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."PowerOutput"'
        verbose_name = 'PowerOutput'
        verbose_name_plural = 'PowerOutputs'
        indexes = []

