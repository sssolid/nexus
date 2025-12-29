from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class CodeMaster(AutocareAPIMetadata, models.Model):
    code_master_id = models.IntegerField(db_column='CodeMasterID', primary_key=True)
    part_terminology = models.ForeignKey('autocare_pcdb.Parts', db_column='PartTerminologyID', db_index=True, on_delete=models.DO_NOTHING)
    category = models.ForeignKey('autocare_pcdb.Categories', db_column='CategoryID', db_index=True, on_delete=models.DO_NOTHING)
    sub_category = models.ForeignKey('autocare_pcdb.Subcategories', db_column='SubCategoryID', db_index=True, on_delete=models.DO_NOTHING)
    position = models.ForeignKey('autocare_pcdb.Positions', db_column='PositionID', db_index=True, on_delete=models.DO_NOTHING)
    rev_date = models.DateField(db_column='RevDate', null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_pcdb'
        managed = True
        db_table = '"autocare_pcdb"."CodeMaster"'
        verbose_name = 'CodeMaster'
        verbose_name_plural = 'CodeMasters'
        indexes = [
            models.Index(fields=['code_master_id']),
        ]

