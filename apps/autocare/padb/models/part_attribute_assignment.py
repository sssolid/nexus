from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class PartAttributeAssignment(AutocareAPIMetadata, models.Model):
    paptid = models.IntegerField(db_column='PAPTID', primary_key=True)
    part_terminology_id = models.IntegerField(db_column='PartTerminologyID')
    paid = models.ForeignKey('autocare_padb.PartAttributes', db_column='PAID', db_index=True, on_delete=models.DO_NOTHING)
    meta = models.ForeignKey('autocare_padb.MetaData', db_column='MetaID', db_index=True, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_padb'
        managed = True
        db_table = '"autocare_padb"."PartAttributeAssignment"'
        verbose_name = 'PartAttributeAssignment'
        verbose_name_plural = 'PartAttributeAssignments'
        indexes = [
            models.Index(fields=['paptid']),
        ]

