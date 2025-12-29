from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class MetaUOMCodeAssignment(AutocareAPIMetadata, models.Model):
    meta_uom_code_assignment_id = models.IntegerField(db_column='MetaUOMCodeAssignmentID', primary_key=True)
    paptid = models.IntegerField(db_column='PAPTID')
    meta_uomid = models.ForeignKey('autocare_padb.MetaUOMCodes', db_column='MetaUOMID', db_index=True, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_padb'
        managed = True
        db_table = '"autocare_padb"."MetaUOMCodeAssignment"'
        verbose_name = 'MetaUOMCodeAssignment'
        verbose_name_plural = 'MetaUOMCodeAssignments'
        indexes = [
            models.Index(fields=['meta_uom_code_assignment_id']),
        ]

