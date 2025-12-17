from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class Changes(AutocareAPIMetadata, models.Model):
    change_id = models.IntegerField(db_column='ChangeID', primary_key=True)
    request_id = models.IntegerField(db_column='RequestID')
    change_reasons = models.ForeignKey('ChangeReasons', db_column='ChangeReasonID', db_index=True, on_delete=models.DO_NOTHING)
    rev_date = models.DateTimeField(db_column='RevDate', blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."changes"'
        verbose_name = 'Changes'
        verbose_name_plural = 'Changes'
        indexes = [
            models.Index(fields=['change_id'])
        ]

