from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class ChangeReasons(AutocareAPIMetadata, models.Model):
    change_reason_id = models.IntegerField(db_column='ChangeReasonID', primary_key=True)
    change_reason = models.CharField(db_column='ChangeReason', max_length=255)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_pcdb'
        managed = True
        db_table = '"autocare_pcdb"."ChangeReasons"'
        verbose_name = 'ChangeReasons'
        verbose_name_plural = 'ChangeReasonss'
        indexes = [
            models.Index(fields=['change_reason_id']),
        ]

