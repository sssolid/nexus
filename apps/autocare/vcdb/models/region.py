from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class Region(AutocareAPIMetadata, models.Model):
    region_id = models.IntegerField(db_column='RegionID', primary_key=True)
    parent_region = models.ForeignKey('autocare_vcdb.Region', db_column='ParentID', blank=True, null=True, db_index=True, on_delete=models.DO_NOTHING, related_name='children')
    region_abbr = models.CharField(db_column='RegionAbbr', max_length=3, blank=True, null=True)
    region_name = models.CharField(db_column='RegionName', max_length=30, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.region_name}"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."region"'
        app_label = 'autocare_vcdb'
        verbose_name = 'Region'
        verbose_name_plural = 'Regions'
        indexes = [
            models.Index(fields=['region_id'])
        ]

