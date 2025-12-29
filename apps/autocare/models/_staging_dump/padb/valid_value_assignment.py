from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class ValidValueAssignment(AutocareAPIMetadata, models.Model):
    valid_value_assignment_id = models.IntegerField(db_column='ValidValueAssignmentID', primary_key=True)
    paptid = models.IntegerField(db_column='PAPTID')
    valid_value = models.ForeignKey('autocare_padb.ValidValues', db_column='ValidValueID', db_index=True, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_padb'
        managed = True
        db_table = '"autocare_padb"."ValidValueAssignment"'
        verbose_name = 'ValidValueAssignment'
        verbose_name_plural = 'ValidValueAssignments'
        indexes = [
            models.Index(fields=['valid_value_assignment_id']),
        ]

