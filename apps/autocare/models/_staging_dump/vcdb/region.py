from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class Region(AutocareAPIMetadata, models.Model):
    region_id = models.IntegerField(db_column='RegionID', primary_key=True)
    parent = models.ForeignKey('autocare_vcdb.Region', db_column='ParentID', db_index=True, on_delete=models.DO_NOTHING)
    region_abbr = models.CharField(db_column='RegionAbbr', max_length=3, null=True, blank=True)
    region_name = models.CharField(db_column='RegionName', max_length=30, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."Region"'
        verbose_name = 'Region'
        verbose_name_plural = 'Regions'
        indexes = [
            models.Index(fields=['region_id']),
        ]

