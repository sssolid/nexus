from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class BrakeConfig(AutocareAPIMetadata, models.Model):
    brake_config_id = models.IntegerField(db_column='BrakeConfigID', primary_key=True)
    front_brake_type = models.ForeignKey('autocare_vcdb.BrakeType', db_column='FrontBrakeTypeID', db_index=True, on_delete=models.DO_NOTHING)
    rear_brake_type = models.ForeignKey('autocare_vcdb.BrakeType', db_column='RearBrakeTypeID', db_index=True, on_delete=models.DO_NOTHING)
    brake_system = models.ForeignKey('autocare_vcdb.BrakeSystem', db_column='BrakeSystemID', db_index=True, on_delete=models.DO_NOTHING)
    brake_absid = models.ForeignKey('autocare_vcdb.BrakeABS', db_column='BrakeABSID', db_index=True, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."BrakeConfig"'
        verbose_name = 'BrakeConfig'
        verbose_name_plural = 'BrakeConfigs'
        indexes = [
            models.Index(fields=['brake_config_id']),
        ]

