from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class PartAttributes(AutocareAPIMetadata, models.Model):
    paid = models.IntegerField(db_column='PAID', primary_key=True)
    pa_name = models.CharField(db_column='PAName', max_length=80, null=True, blank=True)
    pa_descr = models.CharField(db_column='PADescr', max_length=512, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_padb'
        managed = True
        db_table = '"autocare_padb"."PartAttributes"'
        verbose_name = 'PartAttributes'
        verbose_name_plural = 'PartAttributess'
        indexes = [
            models.Index(fields=['paid']),
        ]

