from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class PartTypeStyle(AutocareAPIMetadata, models.Model):
    style_id = models.IntegerField(db_column='StyleID', null=True, blank=True)
    part_terminology_id = models.IntegerField(db_column='PartTerminologyID', null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_padb'
        managed = True
        db_table = '"autocare_padb"."PartTypeStyle"'
        verbose_name = 'PartTypeStyle'
        verbose_name_plural = 'PartTypeStyles'
        indexes = []

