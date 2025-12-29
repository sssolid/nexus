from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class EngineBlock(AutocareAPIMetadata, models.Model):
    engine_block_id = models.IntegerField(db_column='EngineBlockID', primary_key=True)
    liter = models.CharField(db_column='Liter', max_length=6)
    cc = models.CharField(db_column='CC', max_length=8)
    c_id = models.CharField(db_column='CID', max_length=7)
    cylinders = models.CharField(db_column='Cylinders', max_length=2)
    block_type = models.CharField(db_column='BlockType', max_length=2)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."engine_block"'
        app_label = 'autocare_vcdb'
        verbose_name = 'Engine Block'
        verbose_name_plural = 'Engine Blocks'
        indexes = [
            models.Index(fields=['engine_block_id'])
        ]

