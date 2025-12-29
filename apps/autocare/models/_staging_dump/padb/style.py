from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class Style(AutocareAPIMetadata, models.Model):
    style_id = models.IntegerField(db_column='StyleID', null=True, blank=True)
    style_name = models.CharField(db_column='StyleName', max_length=225, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_padb'
        managed = True
        db_table = '"autocare_padb"."Style"'
        verbose_name = 'Style'
        verbose_name_plural = 'Styles'
        indexes = []

