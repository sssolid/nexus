from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class MetaUOMCodes(AutocareAPIMetadata, models.Model):
    meta_uomid = models.IntegerField(db_column='MetaUOMID', primary_key=True)
    uom_code = models.CharField(db_column='UOMCode', max_length=10, null=True, blank=True)
    uom_description = models.CharField(db_column='UOMDescription', max_length=512, null=True, blank=True)
    uom_label = models.CharField(db_column='UOMLabel', max_length=10, null=True, blank=True)
    measurement_group = models.ForeignKey('autocare_padb.MeasurementGroup', db_column='MeasurementGroupID', db_index=True, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_padb'
        managed = True
        db_table = '"autocare_padb"."MetaUOMCodes"'
        verbose_name = 'MetaUOMCodes'
        verbose_name_plural = 'MetaUOMCodess'
        indexes = [
            models.Index(fields=['meta_uomid']),
        ]

