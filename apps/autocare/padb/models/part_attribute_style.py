from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class PartAttributeStyle(AutocareAPIMetadata, models.Model):
    style_id = models.IntegerField(db_column='StyleID', null=True, blank=True)
    paptid = models.ForeignKey('autocare_padb.PartAttributeAssignment', db_column='PAPTID', db_index=True, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_padb'
        managed = True
        db_table = '"autocare_padb"."PartAttributeStyle"'
        verbose_name = 'PartAttributeStyle'
        verbose_name_plural = 'PartAttributeStyles'
        indexes = []

