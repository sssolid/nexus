from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class Changes(AutocareAPIMetadata, models.Model):
    change_id = models.IntegerField(db_column='ChangeID', primary_key=True)
    request_id = models.IntegerField(db_column='RequestID')
    change_reason = models.ForeignKey('autocare_vcdb.ChangeReasons', db_column='ChangeReasonID', db_index=True, on_delete=models.DO_NOTHING)
    rev_date = models.DateTimeField(db_column='RevDate', null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."Changes"'
        verbose_name = 'Changes'
        verbose_name_plural = 'Changess'
        indexes = [
            models.Index(fields=['change_id']),
        ]

