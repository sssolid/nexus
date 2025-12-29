from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class BrakeConfig(AutocareAPIMetadata, models.Model):
    brake_config_id = models.IntegerField(db_column='BrakeConfigID', primary_key=True)
    brake_type = models.ForeignKey('autocare_vcdb.BrakeType', db_column='FrontBrakeTypeID', db_index=True, on_delete=models.DO_NOTHING)
    brake_type = models.ForeignKey('autocare_vcdb.BrakeType', db_column='RearBrakeTypeID', related_name='brakeconfig_rearbraketypeid_set', db_index=True, on_delete=models.DO_NOTHING)
    brake_system = models.ForeignKey('autocare_vcdb.BrakeSystem', db_column='BrakeSystemID', db_index=True, on_delete=models.DO_NOTHING)
    brake_abs = models.ForeignKey('autocare_vcdb.BrakeABS', db_column='BrakeABSID', db_index=True, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."brake_config"'
        app_label = 'autocare_vcdb'
        verbose_name = 'Brake Config'
        verbose_name_plural = 'Brake Configs'
        indexes = [
            models.Index(fields=['brake_config_id'])
        ]

