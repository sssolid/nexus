from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class MfrBodyCode(AutocareAPIMetadata, models.Model):
    mfr_body_code_id = models.IntegerField(db_column='MfrBodyCodeID', primary_key=True)
    mfr_body_code_name = models.CharField(db_column='MfrBodyCodeName', max_length=10)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."MfrBodyCode"'
        verbose_name = 'MfrBodyCode'
        verbose_name_plural = 'MfrBodyCodes'
        indexes = [
            models.Index(fields=['mfr_body_code_id']),
        ]

