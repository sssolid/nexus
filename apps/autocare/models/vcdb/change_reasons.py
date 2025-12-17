from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class ChangeReasons(AutocareAPIMetadata, models.Model):
    change_reason_id = models.IntegerField(db_column='ChangeReasonID', primary_key=True)
    change_reason = models.CharField(db_column='ChangeReason', max_length=255)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."change_reasons"'
        verbose_name = 'Change Reasons'
        verbose_name_plural = 'Change Reasons'
        indexes = [
            models.Index(fields=['change_reason_id'])
        ]

